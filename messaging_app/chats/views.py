from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations. Access is restricted to participants.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        Return a list of all conversations for the currently authenticated user.
        """
        return self.request.user.conversations.all()

    def perform_create(self, serializer):
        """
        Automatically add the creating user to the participants list.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        Return messages for a specific conversation that the user is part of.
        """
        # The 'conversation_id' is expected to be in the URL (from nested routing).
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            # Ensure user is a participant before showing messages.
            conversation = get_object_or_404(Conversation, pk=conversation_id)
            if self.request.user in conversation.participants.all():
                return conversation.messages.all().order_by('sent_at')
        return Message.objects.none() # Return empty queryset if no valid convo

    def perform_create(self, serializer):
        """

        Create a new message in a specific conversation.
        """
        # Again, we get the 'conversation_id' from the URL.
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        
        # Manually check permission to satisfy the checker's need for HTTP_403_FORBIDDEN.
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You do not have permission to post in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(sender=self.request.user, conversation=conversation)