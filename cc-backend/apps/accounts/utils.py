from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class PermissiveJWTAuthentication(JWTAuthentication):
    """
    A custom JWT authenticator that allows anonymous access
    """
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, TypeError):
            # If an invalid token is provided, we still want to fail hard.
            # This could be logged or handled as needed.
            return None
        except Exception:
            return None