"""video_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from video_app.views import listing, login_index, register_index, detail, detail_vote
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout_then_login
from video_app.api import video, video_card, getuser, modifyuser, createuser
from video_app.mobile_view import m_video, userlist, userdetail, userlogin
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', listing, name='list'),
    path('list/<cate>/', listing, name='list'),
    path('m/list/', m_video, name='m_list'),
    path('m/userlist/', userlist, name='userlist'),
    path('m/userlogin/', userlogin, name='userlogin'),
    path('m/userdetail/<id>', userdetail, name='userdetail'),
    path('detail/<id>/', detail, name='detail'),
    path('detail/vote/<id>/', detail_vote, name='vote'),
    path('login/', login_index, name='login'),
    path('register/', register_index, name='register'),
    path('logout/', logout_then_login, {'login_url': '/login'}, name='logout'),
    path('api/videos/', video),
    path('api/videos/<id>', video_card),
    path('api/token-auth', views.obtain_auth_token),
    path('api/users/', getuser),
    path('api/userone/<id>', modifyuser),
    path('api/createuser/', createuser),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)