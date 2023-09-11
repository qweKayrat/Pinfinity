from django.urls import path
from .views import ContentHome, ShowPost, ContentCategory, \
    AddPost, FAQ, SelectQuestions, saved_add, saved_remove

urlpatterns = [
    path('', ContentHome.as_view(), name='index'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ContentCategory.as_view(), name='category'),
    path('addpage/', AddPost.as_view(), name='add_post'),

    path('saved-add/<int:image_id>/', saved_add, name='saved_add'),
    path('saved-remove/<int:image_id>/', saved_remove, name='saved_remove'),

    path('FAQ/', FAQ.as_view(), name='faq'),
    path('FAQ/<int:questions_id>/', SelectQuestions.as_view(), name='questions'),
]
