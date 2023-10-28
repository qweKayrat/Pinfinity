from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q, OuterRef, Subquery, Exists
from django.contrib import messages

from .forms import AddPostForm, ReviewForm, QuestionForm
from .utils import DataMixin, tile_in_slug
from .models import Category, Content, Questions, Answers, SavedImage, Like
from users.models import Subscription


class ContentHome(DataMixin, ListView):
    model = Content
    template_name = 'content/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(cats=True)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user = self.request.user
        # Получаем QuerySet всех постов
        queryset = super().get_queryset()
        if user.is_authenticated:
            # Создаем подзапрос, который проверяет, есть ли SavedImage для данного пользователя и данного поста
            saved_image_subquery = SavedImage.objects.filter(
                user=user,
                content=OuterRef('pk')
            ).values('content_id')[:1]
            queryset = queryset.annotate(saved=Subquery(saved_image_subquery))

        # Добавляем аннотацию к основному QuerySet, чтобы включить флаг "сохранено" для каждого поста

        # Добавляем поиск по запросу, если он задан
        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(owner__username__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(cat__name__icontains=search_query)
            ).distinct()

        return queryset.prefetch_related('cat')


class ContentCategory(DataMixin, ListView):
    model = Content
    template_name = 'content/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Content.objects.filter(cat__slug=self.kwargs["cat_slug"]).prefetch_related('cat')
        user = self.request.user

        if user.is_authenticated:
            saved_image_subquery = SavedImage.objects.filter(
                user=user,
                content=OuterRef('pk')
            ).values('content_id')[:1]

            queryset = queryset.annotate(saved=Subquery(saved_image_subquery))

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            saved_post = SavedImage.objects.filter(user__username=user).select_related('content')
            context.update({'saved_post': saved_post})

        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(selected=c.pk, cats=True)
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView):
    model = Content
    template_name = 'content/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        previous_page = self.request.META.get('HTTP_REFERER')
        user = self.request.user
        saved_post = SavedImage.objects.filter(user__username=user).select_related('content')

        post_owner = self.object.owner
        is_subscriber = False

        subscribers_count = Subscription.objects.count_subscribers(post_owner)
        if user.is_authenticated:
            is_subscriber = Subscription.objects.is_subscriber(user, post_owner)

        context.update({'saved_post': saved_post, 'subscribers_count': subscribers_count,
                        'is_subscriber': is_subscriber, 'form_comment': ReviewForm(),
                        'previous_page': previous_page})

        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        queryset = super().get_queryset().select_related('owner')
        user = self.request.user
        if user.is_authenticated:
            saved_image_subquery = SavedImage.objects.filter(
                user=user,
                content=OuterRef('pk')
            ).values('content_id')[:1]

            liked_post_subquery = Like.objects.filter(
                user=user,
                content=OuterRef('pk')
            ).values('content_id')[:1]

            queryset = queryset.annotate(saved=Subquery(saved_image_subquery), liked=Exists(liked_post_subquery))

        return queryset


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'content/addpost.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_page = self.request.META.get('HTTP_REFERER')
        context['previous_page'] = previous_page
        c_def = self.get_user_context(title='Добавление поста')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        try:
            post = form.save(commit=False)
            post.slug = tile_in_slug(post.title)
            post.owner = self.request.user
            post.save()
            form.save_m2m()
            return redirect('index')
        except Exception as e:
            error_message = f"Ошибка сохранения данных: {str(e)}"
            return HttpResponse(error_message)


def delete_post(request, image_id):
    user = request.user
    image = Content.objects.get(id=image_id)
    if image.owner != user:
        messages.error(request, 'Вы не можете удалить изображение, не являясь его автором')
    elif image is not None:
        image.delete()
        messages.success(request, 'Пост успешно удалён')
    return redirect('profile', user)


class FAQ(DataMixin, ListView):
    model = Answers
    template_name = 'content/faq.html'
    context_object_name = 'answers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(selected=Answers.objects.first().id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Answers.objects.filter(is_published=True)


class SelectAnswer(DataMixin, ListView):
    model = Answers
    template_name = 'content/faq.html'
    context_object_name = 'answers'

    def get_queryset(self):
        return Answers.objects.filter(is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Answers.objects.get(id=self.kwargs["answers_id"])
        c_def = self.get_user_context(selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class AskQuestions(DataMixin, CreateView):
    form_class = QuestionForm
    template_name = 'content/faq.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = Answers.objects.filter(is_published=True)
        c_def = self.get_user_context(ask=True)

        return dict(list(context.items()) + list(c_def.items()))

    # def form_valid(self, form):


class AddComment(LoginRequiredMixin, CreateView):
    form_class = ReviewForm
    template_name = 'content/post.html'
    # success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            comment = form.save(commit=False)
            comment.owner = self.request.user
            comment.content = Content.objects.get(slug=self.kwargs['post_slug'])
            comment.save()
            return redirect(self.request.META.get('HTTP_REFERER'))
        except Exception as e:
            error_message = f"Ошибка сохранения данных: {str(e)}"
            return HttpResponse(error_message)


def saved_add(request, image_id):
    current_page = request.META.get('HTTP_REFERER')
    user = request.user
    if user.is_anonymous:
        messages.error(request, 'Для сохранения изображения необходимо авторизоваться')
    else:
        image = Content.objects.get(id=image_id)
        saved_image = SavedImage.objects.filter(user=user, content=image)
        if not saved_image.exists():
            SavedImage.objects.create(user=user, content=image)
    return redirect(current_page)


def saved_remove(request, image_id):
    current_page = request.META.get('HTTP_REFERER')
    user = request.user
    if user.is_anonymous:
        messages.error(request, 'Для сохранения изображения необходимо авторизоваться')
    else:
        image = Content.objects.get(id=image_id)
        saved_image = SavedImage.objects.filter(user=user, content=image)
        if saved_image.exists():
            saved_image.delete()
    return redirect(current_page)


def like(request, image_id):
    current_page = request.META.get('HTTP_REFERER')
    user = request.user
    if user.is_anonymous:
        messages.error(request, 'Для лайка изображения необходимо авторизоваться')
    else:
        image = Content.objects.get(id=image_id)
        saved_like = Like.objects.filter(user=user, content=image)
        if not saved_like.exists():
            Like.objects.create(user=user, content=image)
            image.get_vote_like()
    return redirect(current_page)


def remove_like(request, image_id):
    current_page = request.META.get('HTTP_REFERER')
    user = request.user
    if user.is_anonymous:
        messages.error(request, 'Для лайка изображения необходимо авторизоваться')
    else:
        image = Content.objects.get(id=image_id)
        saved_like = Like.objects.filter(user=user, content=image)
        if saved_like.exists():
            saved_like.delete()
            image.get_vote_like()
    return redirect(current_page)

# Попытки AJAX подгрузки контента
# def load_more_content(request):
#     offset = int(request.GET.get('offset', 0))
#     cat_slug = int(request.GET.get('cat_slug', False))
#     limit = 20
#     content = Content.objects.all()[offset:offset + limit]
#     user = request.user

# if cat_slug:
#     content = Content.objects.filter(cat__slug=cat_slug)[offset:offset + limit]
#
# saved_image_subquery = SavedImage.objects.filter(
#     user=user,
#     content=OuterRef('pk')
# ).values('content_id')[:1]
#
# content = content.annotate(saved=Subquery(saved_image_subquery))
#
# if user.is_authenticated:
#     saved_image_subquery = SavedImage.objects.filter(
#         user=user,
#         content=OuterRef('pk')
#     ).values('content_id')[:1]
#     content = content.annotate(saved=Subquery(saved_image_subquery))
#
# search_query = request.GET.get('search_query')
# if search_query:
#     content = content.filter(
#         Q(title__icontains=search_query) |
#         Q(owner__username__icontains=search_query) |
#         Q(content__icontains=search_query) |
#         Q(cat__name__icontains=search_query)
#     ).distinct()[offset:offset + limit]

# data = []
# for item in content:
#     data.append({
#         'id': item.id,
#         'title': item.title,
#         'image_url': item.image.url,
#         'slug': item.slug,
#         'owner_username': item.owner.username,
#         'owner_img': item.owner.img.url,
#     })
#
# return JsonResponse(data, safe=False)
