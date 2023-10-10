from django.db import models
from django.urls import reverse
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    img = models.ImageField(upload_to='Tag/&Y/%m/%d/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Content(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    content = models.CharField(max_length=255, blank=True, null=True, verbose_name="Контент")
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name="Изображение")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")
    source_link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка на источник')
    cat = models.ManyToManyField(Category, blank=True, verbose_name="Категории")
    likes = models.IntegerField(default=0, verbose_name="Понравилось")

    def get_vote_like(self):
        like = self.like_set.all()
        total_likes = like.count()
        self.likes = total_likes
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = 'Изображении'
        ordering = ['-time_created']


class SavedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="saved_images", verbose_name="Изображение")
    create_database = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Пользователь {self.user} | Изображение {self.content.title} {self.content.id}'

    class Meta:
        unique_together = ('user', 'content')

        verbose_name = 'сохранённое изображение'
        verbose_name_plural = 'Сохранённые изображения'


class Questions(models.Model):
    PROBLEM = 0
    ERROR = 1
    IMPROVEMENT = 2

    TYPE = (
        (PROBLEM, 'Проблема регистрации/авторизации'),
        (ERROR, 'Ошибка при работе с сайтом'),
        (IMPROVEMENT, 'Предложения по улучшению'),
    )

    type = models.SmallIntegerField(default=PROBLEM, choices=TYPE, verbose_name='тип вопроса')
    title = models.CharField(default=None, max_length=255, verbose_name='Название')
    body = models.TextField(blank=True, null=True, verbose_name="Тело вопроса")
    email = models.EmailField(default=None, null=True, max_length=255, verbose_name='Почта')
    is_answered = models.BooleanField(default=False, verbose_name="Дан ответ")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = 'Вопросы'
        ordering = ['-time_created']


class Answers(models.Model):
    title = models.CharField(default=None, max_length=255, verbose_name='Название')
    body = models.TextField(blank=True, verbose_name="Тело ответа")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_updated = models.DateTimeField(auto_now=True, verbose_name="Дата редактирования")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = 'Ответы'
        ordering = ['-time_updated']


class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    body = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Изображение {self.content.title} | комментарий от {self.owner.username}'

    class Meta:
        verbose_name = 'реакции / комментарии'
        verbose_name_plural = 'Реакция / Комментарий'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ограничение на то, чтобы пользователь не мог лайкать один пост несколько раз
        unique_together = (('user', 'content'),)
