from django.urls import path
from .views import RegisterUser, logout_user, LoginUser, Messages, AddMessage, \
    Chat, ProfileUser, EditProfileUser, subscribe, unsubscribe, load_messages

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('messages/', Messages.as_view(), name='messages'),
    path('add_message/<slug:recipient>', AddMessage.as_view(), name='add-message'),
    path('chat/<slug:sender>/', Chat.as_view(), name='chat'),
    path('load_messages/', load_messages, name='load_messages'),


    path('edit/', EditProfileUser.as_view(), name='edit-profile'),
    path('<slug:username>/', ProfileUser.as_view(), name='profile'),

    path('subscribe/<slug:username>/', subscribe, name='subscribe'),
    path('unsubscribe/<slug:username>/', unsubscribe, name='unsubscribe'),
]
