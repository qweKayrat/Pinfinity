from django.contrib import admin
from .models import Content, Review, Category, Questions, Answers
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class ContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # автоматическое добавление slug по title на стороне admin

    list_display = ("id", "title", 'time_created', 'time_updated', 'image', 'source_link')
    # вывод полей в admin

    list_display_links = ('id', 'title',)
    # ссылки для редактировния в admin

    search_fields = ('id', 'title')
    # поиск по полям в admin

    readonly_fields = ('time_created', 'time_updated')
    # отображение полей в admin без возможности редактирования

    list_filter = ('cat', 'time_created',)
    # фильтрация полей в admin панели


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class AnswersAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Questions
        fields = '__all__'


class AnswersAdmin(admin.ModelAdmin):
    form = AnswersAdminForm
    list_display = ("id", "title", 'time_created', 'time_updated', 'is_published')
    # вывод полей в admin
    list_display_links = ('id', 'title',)
    # ссылки для редактировния в admin
    search_fields = ('title', 'body')
    # поиск по полям в admin
    readonly_fields = ('time_created', 'time_updated')
    # отображение полей в admin без возможности редактирования
    list_editable = ('is_published',)
    # редактирование полей со стороны admin панели
    list_filter = ('time_created', 'is_published',)
    # фильтрация полей в admin панели
    fields = ('title', 'body', 'time_created', 'time_updated', 'is_published',)
    save_on_top = True


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'type', 'time_created', 'is_answered')
    # вывод полей в admin
    list_display_links = ('id', 'type', 'title',)
    # ссылки для редактировния в admin
    search_fields = ('title', 'body', 'type')
    # поиск по полям в admin
    readonly_fields = ('time_created',)
    # отображение полей в admin без возможности редактирования
    list_editable = ('is_answered',)
    # редактирование полей со стороны admin панели
    list_filter = ('time_created', 'is_answered',)
    # фильтрация полей в admin панели
    fields = ('title', 'body', 'type', 'time_created', 'is_answered',)
    save_on_top = True


admin.site.register(Content, ContentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(Review)
