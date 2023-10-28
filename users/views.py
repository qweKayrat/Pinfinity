from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Subquery, OuterRef

from .forms import RegisterUserForm, UserProfileForm, MessageForm
from .models import Message, User, Subscription
from content.models import Content
from content.utils import DataMixin


class ProfileUser(DataMixin, ListView):
    model = User
    template_name = 'users/profile.html'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        previous_page = self.request.META.get('HTTP_REFERER')
        user = self.get_object()
        c_def = self.get_user_context()

        saved_posts_user = Content.objects.filter(saved_images__user__username=self.kwargs['username'])
        subscribers_count = Subscription.objects.count_subscribers(user)

        context.update({'user': user, 'saved_posts': saved_posts_user, 'subscribers_count': subscribers_count,
                        'previous_page': previous_page})

        if self.request.user.is_authenticated:
            saved_current_user = Content.objects.filter(saved_images__user=self.request.user)
            is_subscriber = Subscription.objects.is_subscriber(self.request.user, user)
            context.update({'saved_current': saved_current_user, 'is_subscriber': is_subscriber})

        return dict(list(context.items()) + list(c_def.items()))


class EditProfileUser(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        c_def = self.get_user_context(title='Изменение профиля')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        super().form_valid(form)
        messages.success(self.request, 'Данные были успешно изменены.')
        return super().form_valid(form)


class Messages(LoginRequiredMixin, DataMixin, ListView):
    model = Message
    template_name = 'users/message.html'
    login_url = reverse_lazy('index')
    context_object_name = 'message'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        count_unread_messages = Message.objects.count_unread_messages(self.request.user)
        context['unread_messages'] = count_unread_messages

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        # Подзапрос для получения последних сообщений для каждого отправителя
        latest_messages_subquery = Message.objects.filter(
            recipient=self.request.user,
            sender=OuterRef('sender')
        ).order_by('-created').values('created')[:1]

        # Основной запрос, который выбирает сообщения, удовлетворяющие подзапросу
        queryset = Message.objects.filter(
            recipient=self.request.user,
            created=Subquery(latest_messages_subquery)
        ).select_related('sender').order_by('is_read', '-created')

        return queryset


class Chat(LoginRequiredMixin, DataMixin, ListView):
    model = Message
    template_name = 'users/chat.html'
    context_object_name = 'message'
    # временно, пока не разобрался с Ajax
    paginate_by = 9999

    def get_login_url(self):
        # Используйте resolve_url для динамического sender
        return reverse_lazy('profile', kwargs={'username': self.kwargs['sender']})

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, был ли пользователь перенаправлен из-за отсутствия аутентификации
        if not request.user.is_authenticated:
            messages.error(request, f'Для того чтобы написать {self.kwargs["sender"]} нужно авторизоваться')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_page = self.request.META.get('HTTP_REFERER')
        context['previous_page'] = previous_page

        c_def = self.get_user_context(form=MessageForm(), sender=self.kwargs['sender'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        sender = User.objects.get(username=self.kwargs['sender'])
        queryset = Message.objects.filter(
            Q(recipient__username=user, sender__username=sender) |
            Q(recipient__username=sender, sender__username=user)
        ).select_related('sender', 'recipient')

        Message.objects.mark_messages_as_read(sender=sender, recipient=user)
        return queryset


class AddMessage(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = 'users/chat.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            message = form.save(commit=False)
            message.sender = self.request.user
            message.recipient = User.objects.get(username=self.kwargs['recipient'])
            print(message.recipient)
            print(message.sender)
            message.save()
            return redirect(self.request.META.get('HTTP_REFERER'))
        except Exception as e:
            error_message = f"Ошибка сохранения данных: {str(e)}"
            return HttpResponse(error_message)


def load_messages(request):
    sender = str(request.GET.get('sender_username', False))
    messages = Message.objects.filter(recipient__username=request.user,
                                      sender__username=sender).select_related('sender', 'recipient')
    data = [{'body': message.body, 'created': message.created, 'sender': message.sender.username} for message in messages]
    return JsonResponse({'messages': data})


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


def logout_user(request):
    logout(request)
    return redirect('index')


# Логика подписки / отписки
def subscribe(request, username):
    current_page = request.META.get('HTTP_REFERER')
    user = request.user

    if user.is_anonymous:
        messages.error(request, 'Для подписки необходимо авторизоваться')
    elif username == user.username:
        messages.error(request, 'Нельзя подписаться на самого себя')
    else:
        target_user = User.objects.get(username=username)
        subscriber = Subscription.objects.filter(subscriber=user, target_user=target_user)
        if not subscriber.exists():
            Subscription.objects.create(subscriber=user, target_user=target_user)
    return redirect(current_page)


def unsubscribe(request, username):
    current_page = request.META.get('HTTP_REFERER')
    user = request.user
    if user.is_anonymous:
        messages.error(request, 'Для подписки необходимо авторизоваться')

    else:
        target_user = User.objects.get(username=username)
        subscriber = Subscription.objects.filter(subscriber=user, target_user=target_user)
        if subscriber.exists():
            subscriber.delete()
    return redirect(current_page)


# Страницы восстановления пароля
class CustomPasswordResetView(DataMixin, auth_views.PasswordResetView):
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))


class CustomPasswordResetConfirmView(DataMixin, auth_views.PasswordResetConfirmView):
    template_name = 'users/reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))


class CustomPasswordResetCompleteView(DataMixin, auth_views.PasswordResetCompleteView):
    template_name = 'users/reset_password_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))
