
"""
Django REST framework middlewares.
"""
from django.apps import apps
from .base import HeaderAuthTokenMiddleware


class DRFAuthTokenMiddlewareMixin:
    """Django REST framework auth token middleware mixin."""

    async def aget_drf_user_instance(self, token_key):
        Token = apps.get_model("authtoken", "Token")
        try:
            token = await Token.objects.select_related("user").aget(key=token_key)
        except Token.DoesNotExist:
            return None
        return token.user


class DRFAuthTokenMiddleware(HeaderAuthTokenMiddleware, DRFAuthTokenMiddlewareMixin,):
    """
    Django REST framework auth token middleware.
    https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    """

    header_name = "Authorization"
    keyword = "Token"
    token_regex = "[0-9a-f]{40}"

    async def get_user_instance(self, token_key):
        return await self.aget_drf_user_instance(token_key)