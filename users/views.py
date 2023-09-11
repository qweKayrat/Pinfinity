from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView
from content.utils import DataMixin
from .forms import RegisterUserForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from .models import Message, User
from django.contrib.auth.mixins import LoginRequiredMixin
from content.models import SavedImage
from django.shortcuts import get_object_or_404
from django.contrib.auth import views as auth_views


class ProfileUser(DataMixin, ListView):
    model = User
    template_name = 'users/profile.html'
    login_url = reverse_lazy('index')
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        c_def = self.get_user_context()
        saved_post = SavedImage.objects.filter(user__username=self.kwargs['username']).select_related('content')
        context.update({'user': user})
        context.update(c_def)
        context.update({'saved_post': saved_post})
        return context


class Messages(LoginRequiredMixin, DataMixin, ListView):
    model = Message
    template_name = 'users/message.html'
    login_url = reverse_lazy('index')
    context_object_name = 'messages'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Message.objects.filter(recipient__username=self.request.user).select_related('sender', 'recipient')


class Chat(LoginRequiredMixin, DataMixin, ListView):
    model = Message
    template_name = 'users/chat.html'
    login_url = reverse_lazy('index')
    context_object_name = 'messages'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Message.objects.filter(recipient__username=self.request.user).select_related('sender', 'recipient')

    # def form_valid(self, form):


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
