from .models import Category, Questions
from django.db.models import Count
import uuid
from slugify import slugify
from transliterate import translit

full_menu = [
    {'title': "Главная", 'url_name': 'index'},
    {'title': "Создать", 'url_name': 'add_post'},
    {'title': "FAQ", 'url_name': 'faq'},
    {'title': "Сообщения", 'url_name': 'messages'},
    {'title': "Аккаунт", 'url_name': 'profile'},
    {'title': "Выйти", 'url_name': 'logout'},
]

limited_menu = [
    {'title': "Главная", 'url_name': 'index'},
    {'title': "FAQ", 'url_name': 'faq'},
    {'title': "Войти", 'url_name': 'login'},
]


class DataMixin:
    paginate_by = 20

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('content'))
        if not self.request.user.is_authenticated:
            user_menu = limited_menu.copy()
        else:
            user_menu = full_menu.copy()

        context['menu'] = user_menu

        if 'cats' in context:
            context['cats'] = cats

        if 'selected' not in context:
            context['selected'] = 0

        context['search_query'] = self.request.GET.get('search_query', '')

        return context


def tile_in_slug(title):
    "Функция для преобразования передаваемого аргумента в slug."

    translit_title = translit(title, 'ru', reversed=True)
    uniq = f"{translit_title}-{str(uuid.uuid4())[-7:]}"
    slug = slugify(uniq, allow_unicode=True)
    # if not content:
    #     slug = slugify(translit_title,  allow_unicode=True)
    # else:
    return slug
