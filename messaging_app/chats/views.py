from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or created.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Add filtering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['participants'] # Filter by participants
    search_fields = ['messages__message_body'] # Search within message content
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        This view should return a list of all the conversations
        for the currently authenticated user.
        """
        user = self.request.user
        return user.conversations.all().prefetch_related('participants', 'messages')

    def get_serializer_context(self):
        """
        Pass the request context to the serializer.
        This is needed for the custom create method in the serializer.
        """
        return {'request': self.request}


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or created.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Add filtering capabilities
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conversation'] # Filter messages by conversation
    ordering_fields = ['sent_at']
    ordering = ['-sent_at'] # Default order is newest first

    def get_queryset(self):
        """
        This view should only return messages in conversations
        that the currently authenticated user is a part of.
        """
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def perform_create(self, serializer):
        """
        Set the sender of the message to the currently authenticated user.
        """
        serializer.save(sender=self.request.user)