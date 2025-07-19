from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from chats.views import MessageViewSet, ConversationViewSet

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
