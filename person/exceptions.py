from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger("django.request")


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to return formatted error responses.
    Handles 500 and other system-level exceptions gracefully.
    """

    # Call the default DRF exception handler first
    response = exception_handler(exc, context)

    if response is None:
        # Handle system-level exceptions (500 errors)
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return Response(
            {"error": "A server error occurred. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Customize error response format
    response.data = {
        "success": False,
        "error": response.data
    }

    return response
