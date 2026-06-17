from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.jwt_utils import verify_token, SECRET_KEY
from accounts.models import User


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header: return None
        try:
            type_, token = header.split()
        except ValueError:
            raise AuthenticationFailed('Noto\'g\'ri format')
        if type_.lower() != 'bearer':
            raise AuthenticationFailed('Bearer kerak')
        payload = verify_token(token, SECRET_KEY)
        if not isinstance(payload, dict):
            raise AuthenticationFailed(payload)

        print(payload)
        user = User.objects.get(id=payload['user_id'])
        return (user, None)
