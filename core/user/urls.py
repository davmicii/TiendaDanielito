from django.urls import path

from core.user.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserProfileView

app_name = 'user'

urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]