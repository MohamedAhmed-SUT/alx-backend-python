from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class HealthCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'status': 'Chats app is active'})
