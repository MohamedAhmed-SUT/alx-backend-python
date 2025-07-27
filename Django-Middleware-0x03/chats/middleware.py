# Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime

# Configure a logger specifically for our requests.
# This will write to a file named 'requests.log' in the project's root directory.
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'  # We only want the message, not extra logger info
)

class RequestLoggingMiddleware:
    """
    A custom middleware that logs details about each incoming request to a file.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called for each request.
        """
        # Determine the user for the log message.
        # If the user is authenticated, use their username. Otherwise, use 'Anonymous'.
        user = request.user if request.user.is_authenticated else 'AnonymousUser'

        # The log message format as required by the instructions.
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"

        # Use the configured logger to write the message to the file.
        logging.info(log_message)

        # Call the next middleware or the view.
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called. We don't need any for this task.

        return response