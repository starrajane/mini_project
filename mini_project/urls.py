"""mini_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from community_blog import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('community_blog.urls')),
    path('me/', views.current_user),
    path('posts/', views.get_all_posts),
    path('posts/<int:id>', views.get_post),
    path('me/posts/', views.get_user_post),

    #path('posts/<int:id>/comments', views.add_comment),

    path('api/users/', views.ListUsers.as_view()),
    path('auth/signup/', views.Register.as_view()),
    path('auth/login/', views.CustomAuthToken.as_view()),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
