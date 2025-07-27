# in Django-Middleware-0x03/messaging_app/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Your custom middleware classes
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.RequestLoggingMiddleware',
]# in Django-Middleware-0x03/messaging_app/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Add your custom middleware here
    'chats.middleware.RequestLoggingMiddleware', 
]
# In Django-Middleware-0x03/settings.py (add this at the bottom)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
# In Django-Middleware-0x03/settings.py

MIDDLEWARE = [
    # ... other middleware
    
    # Your custom middleware classes
    'chats.middleware.OffensiveLanguageMiddleware', # Add this new one
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.RequestLoggingMiddleware',
]
# in Django-Middleware-0x03/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # This middleware adds request.user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Your custom middleware
    # Role check should be one of the first custom checks.
    'chats.middleware.RolePermissionMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.RequestLoggingMiddleware',
]