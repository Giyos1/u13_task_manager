from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from accounts.jwt_utils import verify_token, SECRET_KEY


@database_sync_to_async
def get_user(user_id):
    User = get_user_model()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        qs = scope["query_string"].decode()
        params = parse_qs(qs)
        token = params.get("token", [None])[0]

        payload = verify_token(token, secret=SECRET_KEY)

        # verify_token xatoda dict emas (None yoki "Token expired" kabi str) qaytaradi
        if isinstance(payload, dict):
            scope["user"] = await get_user(payload.get("user_id"))
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)