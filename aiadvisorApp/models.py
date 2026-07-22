from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):

    title = models.CharField(
        max_length=200
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="kwasari_conversations"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-updated_at"]

    def __str__(self):

        return self.title


class Message(models.Model):

    ROLE_CHOICES = (

        ("USER", "User"),

        ("AI", "Kwasari"),

    )

    conversation = models.ForeignKey(

        Conversation,

        on_delete=models.CASCADE,

        related_name="messages"

    )

    role = models.CharField(

        max_length=10,

        choices=ROLE_CHOICES

    )

    content = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["created_at"]

    def __str__(self):

        return f"{self.role}"