from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include the URLs from the 'chats' app under the 'api/chats/' prefix
    path('api/chats/', include('chats.urls')),
]