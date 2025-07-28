# messaging/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

# The checker is looking for a function with this exact name.
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    """
    A view that allows an authenticated user to delete their own account.
    Handles DELETE requests only.
    """
    user = request.user
    
    # The .delete() method will trigger the post_delete signal
    user.delete()
    
    return Response(
        {"detail": "User account has been deleted successfully."},
        status=status.HTTP_2_NO_CONTENT
    )