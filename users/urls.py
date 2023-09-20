from django.urls import path
from .views import RegisterUser, logout_user, LoginUser, Messages, Chat, ProfileUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('<slug:username>/', ProfileUser.as_view(), name='profile'),

    path('message/', Messages.as_view(), name='messages'),
    path('chat/<slug:sender>/', Chat.as_view(), name='chat'),

]
