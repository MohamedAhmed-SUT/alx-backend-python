from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all messages for the logged-in user and create new messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all messages
        sent by or received by the currently authenticated user.
        """
        user = self.request.user
        return Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user))

    def perform_create(self, serializer):
        """
        Set the sender of the message to the currently authenticated user.
        """
        serializer.save(sender=self.request.user)