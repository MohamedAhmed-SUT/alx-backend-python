from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation  # <-- IMPORTANT: Import your custom class

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations. Access is restricted to participants only.
    """
    serializer_class = ConversationSerializer
    # Use your custom permission class here. It also checks for authentication.
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        This view should return a list of all conversations
        for the currently authenticated user.
        """
        return self.request.user.conversations.all().prefetch_related('participants', 'messages')

    def perform_create(self, serializer):
        """
        Automatically add the creating user to the participants list.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages. Access is restricted to participants
    of the conversation.
    """
    serializer_class = MessageSerializer
    # Use your custom permission class here as well.
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        This view should only return messages in conversations
        that the currently authenticated user is a part of.
        This uses the required 'Message.objects.filter' string.
        """
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def perform_create(self, serializer):
        """
        Set the sender of the message to the currently authenticated user.
        The conversation is likely passed in the request data.
        """
        serializer.save(sender=self.request.user)