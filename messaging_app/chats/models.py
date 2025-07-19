import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This model includes all standard Django user fields and adds custom ones.
    The 'password' field is inherited from AbstractUser and handles hashing.
    """
    class Role(models.TextChoices):
        GUEST = 'GUEST', 'Guest'
        HOST = 'HOST', 'Host'
        ADMIN = 'ADMIN', 'Admin'

    # The project asks for 'user_id' but Django's convention is 'id'.
    # We will use 'id' to maintain compatibility with the framework.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Add the custom fields required by the specification.
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)

    # Note: 'first_name', 'last_name', 'email' are already part of AbstractUser.
    # The 'created_at' field is covered by 'date_joined' in AbstractUser.

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """Tracks which users are involved in a conversation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Use settings.AUTH_USER_MODEL to refer to the active User model.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation involving {self.participants.count()} users"


class Message(models.Model):
    """A single message sent by a user within a conversation."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username}"