# messaging/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class DeleteUserView(APIView):
    """
    An endpoint for an authenticated user to delete their own account.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Handles the DELETE request to delete the user's account.
        """
        user = request.user
        # The 'delete()' method on the user model will trigger the
        # post_delete signal we are about to create.
        user.delete()
        return Response(
            {"detail": "User account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )