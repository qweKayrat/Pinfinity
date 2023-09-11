from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class ContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # автоматическое добавление slug по title на стороне admin

    list_display = ("id", "title", 'time_created', 'time_updated', 'image', 'source_link')
    # вывод полей в admin

    list_display_links = ('id', 'title',)
    # ссылки для редактировния в admin

    search_fields = ('title', 'content', 'owner')
    # поиск по полям в admin

    readonly_fields = ('time_created', 'time_updated')
    # отображение полей в admin без возможности редактирования

    list_filter = ('title', 'time_created',)
    # фильтрация полей в admin панели


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class QuestionsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Questions
        fields = '__all__'


class QuestionsAdmin(admin.ModelAdmin):
    form = QuestionsAdminForm
    list_display = ("id", "title", 'time_created', 'time_updated', 'is_published')
    # вывод полей в admin
    list_display_links = ('id', 'title',)
    # ссылки для редактировния в admin
    search_fields = ('title', 'content')
    # поиск по полям в admin
    readonly_fields = ('time_created', 'time_updated')
    # отображение полей в admin без возможности редактирования
    list_editable = ('is_published',)
    # редактирование полей со стороны admin панели
    list_filter = ('time_created', 'is_published',)
    # фильтрация полей в admin панели
    fields = ('title', 'content', 'time_created', 'time_updated', 'is_published',)
    save_on_top = True


admin.site.register(Content, ContentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Questions, QuestionsAdmin)
