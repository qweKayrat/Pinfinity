from django.urls import path
from .views import ContentHome, ShowPost, ContentCategory, \
    AddPost, FAQ, SelectAnswer, saved_add, saved_remove, \
    AddComment, AskQuestions, like, remove_like

urlpatterns = [
    path('', ContentHome.as_view(), name='index'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ContentCategory.as_view(), name='category'),
    path('addpage/', AddPost.as_view(), name='add_post'),

    path('saved-add/<int:image_id>/', saved_add, name='saved_add'),
    path('saved-remove/<int:image_id>/', saved_remove, name='saved_remove'),

    path('like/<int:image_id>/', like, name='like'),
    path('remove-like/<int:image_id>/', remove_like, name='remove-like'),

    path('comment/<slug:post_slug>/', AddComment.as_view(), name='comment'),

    path('FAQ/', FAQ.as_view(), name='faq'),
    path('FAQ/<int:answers_id>/', SelectAnswer.as_view(), name='answers'),
    path('FAQ/ask', AskQuestions.as_view(), name='ask'),

    # path('load_more_content/', load_more_content, name='load_more_content'),
]
