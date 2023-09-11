from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .forms import AddPostForm
from .utils import DataMixin, tile_in_slug
from .models import Category, Content, Questions, SavedImage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages


class ContentHome(DataMixin, ListView):
    model = Content
    template_name = 'content/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        saved_post = SavedImage.objects.filter(user__username=self.request.user).select_related('content')
        context.update({'saved_post': saved_post})

        c_def = self.get_user_context(cats=True)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            return Content.objects.distinct().filter(
                Q(title__icontains=search_query) |
                Q(owner__username__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(cat__name__icontains=search_query)
            ).prefetch_related('cat')
        return Content.objects.prefetch_related('cat')


class ContentCategory(DataMixin, ListView):
    model = Content
    template_name = 'content/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Content.objects.filter(cat__slug=self.kwargs["cat_slug"]).prefetch_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        saved_post = SavedImage.objects.filter(user__username=self.request.user).select_related('content')
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
        saved_post = SavedImage.objects.filter(user__username=self.request.user).select_related('content')
        context.update({'saved_post': saved_post})

        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'content/addpost.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context()
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


class FAQ(DataMixin, ListView):
    model = Questions
    template_name = 'content/faq.html'
    context_object_name = 'questions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(selected=Questions.objects.first().id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Questions.objects.filter(is_published=True)


class SelectQuestions(DataMixin, ListView):
    model = Questions
    template_name = 'content/faq.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return Questions.objects.filter(is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Questions.objects.get(id=self.kwargs["questions_id"])
        c_def = self.get_user_context(selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


def saved_add(request, image_id):
    current_page = request.META.get('HTTP_REFERER')
    user = request.user
    if user.is_anonymous:
        messages.error(request, 'Для сохранения изображения необходимо авторизоваться')
    else:
        image = Content.objects.get(id=image_id)
        saved_image = SavedImage.objects.filter(user=user, content=image)
        if not saved_image.exists():
            SavedImage.objects.create(user=user, image=image)
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
