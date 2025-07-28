from django.db import models
from django.conf import settings

# --- Custom Manager and QuerySet for this task ---
class UnreadMessagesQuerySet(models.QuerySet):
    """
    A custom QuerySet for the Message model that adds a method
    to filter for unread messages for a specific user.
    """
    def for_user(self, user):
        """
        Returns unread messages for a given user.
        This query is optimized with .only() to fetch just the necessary fields.
        """
        return self.filter(receiver=user, is_read=False).only(
            'id', 'sender', 'content', 'timestamp'
        )

class UnreadMessagesManager(models.Manager):
    """
    A custom Manager for the Message model that provides access
    to the UnreadMessagesQuerySet.
    """
    def get_queryset(self):
        return UnreadMessagesQuerySet(self.model, using=self._db)

    def for_user(self, user):
        """
        A convenience method to call the QuerySet's for_user method.
        Example usage: Message.unread.for_user(request.user)
        """
        return self.get_queryset().for_user(user)

# --- Updated Message Model ---
class Message(models.Model):
    """

    Represents a direct message, now with a read status and a custom manager.
    """
    # ... (keep existing fields: sender, receiver, content, timestamp, edited, parent_message) ...
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    
    # NEW FIELD FOR THIS TASK
    is_read = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    
    # ATTACH THE MANAGERS
    objects = models.Manager() # The default manager
    unread = UnreadMessagesManager() # Our new custom manager

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

# ... (Keep your Notification and MessageHistory models as they are) ...
class Notification(models.Model):
    #...
    pass

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"History for Message {self.message.id}"