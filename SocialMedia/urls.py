from .import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index,name='index'),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("like_post",views.like_post,name="like_post"),
    path("follow_profile/<profile_id>",views.follow_profile,name="follow_profile"),
    path('settings',views.settings,name='settings'),
    path("delete/<post_id>",views.delete,name="delete"),
    path('search',views.search,name='search'),
    path("profile/<int:pk>",views.profile,name="profile"),
    path("logout",auth_views.LogoutView.as_view(template_name='signin.html'),name="logout")
]
