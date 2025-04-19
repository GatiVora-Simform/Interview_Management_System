from django.urls import path
# from account.api.views import registration_view
from account.api.views import (UserCreateView, 
    UserDetailView,
    UserListView,
    UserProfileView,)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
