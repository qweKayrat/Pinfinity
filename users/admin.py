from django.contrib import admin
from .models import User, Message


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", 'first_name', 'email', 'last_login', 'is_superuser')
    # вывод полей в admin

    list_display_links = ('id', 'username', 'first_name')
    # ссылки для редактировния в admin

    search_fields = ('id', 'username', 'email')
    # поиск по полям в admin

    readonly_fields = ('last_login',)
    # отображение полей в admin без возможности редактирования

    list_editable = ('is_superuser',)
    # редактирование полей со стороны admin панели

    list_filter = ('last_login', 'is_superuser',)
    # фильтрация полей в admin панели

    # fields = ('')
    # вывод полей
    # save_on_top = True


admin.site.register(User, UserAdmin)
admin.site.register(Message)
