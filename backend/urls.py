"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from backend import views as backend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls')),
    path('incident/', include('apps.incident.urls')),
    path('login/',
        auth_views.LoginView.as_view(
            template_name='user/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    path('logout/',
        auth_views.LogoutView.as_view(
            template_name='user/logout.html',
            # http_method_names = ['get', 'post', 'options']
            # todo - GET method should not be needed, fix this.
        ),
        name='logout'
    ),
    path('help/',
        backend_views.help,
        name='backend_help'
    ),
    path('project/',
        backend_views.project,
        name='backend_project'
    ),
    path('booklet/',
        backend_views.conservation_booklet,
        name='backend_conservation_booklet'
    ),
    path('',
        backend_views.home,
        name='backend_home'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = backend_views.error_404
handler500 = backend_views.error_500
