# in messaging/urls.py
from django.urls import path
from .views import delete_user, ThreadedConversationView

urlpatterns = [
    path('users/delete/', delete_user, name='delete-user'),
    # Add a URL for the new view
    path('thread/', ThreadedConversationView.as_view(), name='threaded-conversation'),
]