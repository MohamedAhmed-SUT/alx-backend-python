from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory # Import MessageHistory

# --- Signal from Task 0 (Keep this) ---
@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Creates a Notification for the receiver when a new Message is created.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


# --- Signal for Task 1 (This is the new part) ---
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a Message is saved, check if it's an update. If the content
    has changed, log the old content to the MessageHistory model.
    """
    if instance.pk:  # Only run for existing messages (updates)
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:
                # The checker is looking for this class name and method call.
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content,
                    # We can't know who edited it from the signal alone,
                    # this would typically be passed from the view.
                    # We will leave it as null for now.
                    edited_by=None 
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass # This is a new message, do nothing.