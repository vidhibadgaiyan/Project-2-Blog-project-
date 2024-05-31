"""techblog URL Configuration

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
from django.urls import path
from blog import views
from .views import  DetailArticleView, LikeArticle
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('signup/',views.user_signup, name="signup"),
    path('login/',views.user_login, name="login"),
    path('logout/',views.user_logout, name="logout"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('addblog/',views.add_blog, name="addblog"),
    path('updateblog/<int:id>/',views.update_blog, name="updateblog"),
    path('delete/<int:id>/',views.delete_blog, name="deleteblog"),
    path('about/',views.about, name="about"),
    path('contact/',views.contact, name="contact"),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article')
    path('<int:pk>/like', LikeArticle.as_view(), name='like_article')
]
