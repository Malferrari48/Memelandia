from django.urls import path
from users.views import UserCreateView
from django.contrib.auth import views as auth_views
from .views import accept_friend_request, listRequestsAccept, listRequestsSend, profile, profile_update, send_friend_request, listFriends

app_name='users'

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile_update/', profile_update, name="profile_update"),
    path('profile/',profile,name="profile"),
    path('possible_friends/', listRequestsSend, name="possible_friends"),
    path('accept_possible_friends/', listRequestsAccept, name="accept_possible_friends"),
    path('friends_list/', listFriends, name="friends_list"),
    path('send_friend_request/<int:userID>/', send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/',accept_friend_request,name = 'accept_friend_request'),
]  
