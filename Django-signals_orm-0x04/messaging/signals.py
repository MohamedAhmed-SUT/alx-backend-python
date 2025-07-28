from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

# The @receiver decorator connects this function to the post_save signal
# for the Message model.
@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    This signal handler is triggered whenever a Message instance is saved.
    It creates a Notification for the receiver if the message is newly created.
    """
    # The 'created' argument is a boolean. It's True only if a new record
    # was created in the database. This prevents notifications from being
    # created when a message is just being updated.
    if created:
        Notification.objects.create(
            user=instance.receiver,  # The user to notify is the receiver of the message
            message=instance         # Link the notification to the message that was just created
        )
        print(f"Signal processed: Notification created for {instance.receiver.username}")