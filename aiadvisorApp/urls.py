from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "ai"

urlpatterns = [

    path(
        "kwasari/",
        views.chat,
        name="kwasari",
    ),

    path(
        "kwasari/new/",
        views.new_conversation,
        name="new_conversation",
    ),

    path(
        "kwasari/<int:conversation_id>/",
        views.chat,
        name="conversation",
    ),

    path(
        "kwasari/send/",
        views.send_message,
        name="send_message",
    ),
    path(
    "accounts/signup/",
    views.signup,
    name="signup",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout"
    ),
]