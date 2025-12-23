from django.urls import path
from apps.user.views import (
    watcher_home,
    coordinator_home,
    manager_home,
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserUpdatePasswordView,
)


urlpatterns = [
    path('watcher/',
        watcher_home,
        name='watcher_home'
    ),
    path('coordinator/',
        coordinator_home,
        name='coordinator_home'
    ),
    path('manager/',
        manager_home,
        name='manager_home'
    ),
    path(
        '',
        UserListView.as_view(),
        name='user_home'
    ),
    path(
        '<int:pk>/',
        UserDetailView.as_view(),
        name='user_detail'
    ),
    path(
        'new/',
        UserCreateView.as_view(),
        name='user_create'
    ),
    path(
        '<int:pk>/update/',
        UserUpdateView.as_view(),
        name='user_update'
    ),
    path(
        '<int:pk>/delete/',
        UserDeleteView.as_view(),
        name='user_delete'
    ),
    path(
        '<int:pk>/update_password/',
        UserUpdatePasswordView.as_view(),
        name='user_update_password'
    ),
]
