from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("page/<int:page_id>", views.page, name="page"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("newpost", views.newpost, name="newpost"),
]