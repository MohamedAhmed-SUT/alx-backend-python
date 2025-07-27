# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsParticipantInConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view it or its related messages.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        The 'obj' can be either a Conversation or a Message instance.
        """
        # If the object is a Message, we check its parent conversation.
        # If it's a Conversation, we check it directly.
        conversation = obj if hasattr(obj, 'participants') else obj.conversation
        
        # The check: is the requesting user in the list of participants?
        return request.user in conversation.participants.all()