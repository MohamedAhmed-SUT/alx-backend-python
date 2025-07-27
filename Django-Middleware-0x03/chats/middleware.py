# Add these imports at the top of chats/middleware.py
import time
from django.http import JsonResponse
from django.core.cache import cache

# ... (keep your existing RequestLoggingMiddleware and RestrictAccessByTimeMiddleware) ...


# --- New Middleware for this task ---
class OffensiveLanguageMiddleware: # Note: Name is based on instructions, logic is rate limiting
    """
    Middleware that limits the number of POST requests (chat messages)
    a user can send from a specific IP address within a time window.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # We will allow 5 requests per 60 seconds (1 minute)
        self.limit = 5
        self.period = 60

    def __call__(self, request):
        # This middleware should only apply to the message creation endpoint.
        # Let's assume this is a POST request to a path ending in '/messages/'.
        if request.method == 'POST' and 'messages' in request.path:
            # Get the client's IP address
            ip_address = request.META.get('REMOTE_ADDR')
            if not ip_address:
                # Should not happen in a real scenario, but handle it.
                return JsonResponse(
                    {'error': 'Could not identify client IP.'},
                    status=400
                )

            # Use Django's cache to store request timestamps for each IP
            cache_key = f"rate_limit_{ip_address}"
            request_timestamps = cache.get(cache_key, [])

            # Get the current time
            current_time = time.time()
            
            # Filter out timestamps that are older than our time window (self.period)
            valid_timestamps = [
                ts for ts in request_timestamps if current_time - ts < self.period
            ]

            # Check if the number of recent requests exceeds the limit
            if len(valid_timestamps) >= self.limit:
                return JsonResponse(
                    {'error': 'Request limit exceeded. Please try again later.'},
                    status=429  # 429 Too Many Requests is the standard status code
                )
            
            # Add the current request's timestamp and update the cache
            valid_timestamps.append(current_time)
            cache.set(cache_key, valid_timestamps, self.period)

        # If not a message POST or if the limit is not exceeded, proceed
        response = self.get_response(request)
        return response