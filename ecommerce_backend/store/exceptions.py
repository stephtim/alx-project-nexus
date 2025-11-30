from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for standardized error responses.
    Returns consistent error format across all API endpoints.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data format
        custom_response_data = {
            "success": False,
            "error": {
                "status_code": response.status_code,
                "message": None,
                "details": None
            }
        }

        # Extract error message
        if isinstance(response.data, dict):
            # Handle dict response (most common case)
            if "detail" in response.data:
                custom_response_data["error"]["message"] = str(response.data["detail"])
            elif "non_field_errors" in response.data:
                custom_response_data["error"]["message"] = str(response.data["non_field_errors"])
            else:
                # For other field errors, compile them
                error_messages = []
                for field, errors in response.data.items():
                    if isinstance(errors, list):
                        error_messages.append(f"{field}: {', '.join(str(e) for e in errors)}")
                    else:
                        error_messages.append(f"{field}: {errors}")
                custom_response_data["error"]["message"] = "; ".join(error_messages)
                custom_response_data["error"]["details"] = response.data
        elif isinstance(response.data, list):
            # Handle list response
            custom_response_data["error"]["message"] = "; ".join(str(e) for e in response.data)
        else:
            # Handle string response
            custom_response_data["error"]["message"] = str(response.data)

        response.data = custom_response_data

    return response
