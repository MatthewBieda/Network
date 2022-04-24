from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index.as_view(), name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("index/<int:id>", views.profile, name="profile"),
    path("following/", views.following, name="following")
]
