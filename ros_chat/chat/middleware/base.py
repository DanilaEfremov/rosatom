import re

from django.contrib.auth.models import AnonymousUser
from django.utils.functional import empty

from channels.auth import AuthMiddleware, UserLazyObject

class BaseAuthTokenMiddleware(AuthMiddleware):
    """
    Base middleware which populates scope["user"] by authorization token key.
    Could be used behind other auth middlewares like AuthMiddleware.
    """

    # regex need to fullmatch token key
    token_regex = r".*"

    def __init__(self, *args, token_regex=None, **kwargs):
        self.token_regex = str(token_regex or self.token_regex)
        super().__init__(*args, **kwargs)

    def populate_scope(self, scope):
        # Add it to the scope if it is not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        # Get user instance if it is not already in the scope.
        if scope["user"]._wrapped is empty or scope["user"].is_anonymous:
            scope["user"]._wrapped = await self.get_user(scope)

    async def get_user(self, scope):
        token_key_string = self.get_token_key_string(scope)
        if not token_key_string:
            return AnonymousUser()

        token_key = self.parse_token_key(token_key_string)
        if not token_key:
            return AnonymousUser()

        user = await self.get_user_instance(token_key)
        return user or AnonymousUser()

    def get_token_key_string(self, scope):
        """
        Must be implemented by subclass
        to get token key string from the scope.
        Implementation need to return string to parse token key from or None.
        """
        raise NotImplementedError(
            "subclasses of BaseAuthTokenMiddleware "
            "must provide a get_token_key_string(scope) method")

    def parse_token_key(self, token_key_string):
        matched = re.fullmatch(self.token_key_string_regex, token_key_string)
        if not matched:
            return None
        return matched.group(1)

    @property
    def token_key_string_regex(self):
        """
        Regex to parse token key from token key string.
        Token key need to be in first group.
        """

        return rf"({self.token_regex})"

    async def get_user_instance(self, token_key):
        """
        Must be implemented by subclass to get user instance by token key.
        Implementation need to return user instance or None.
        """
        raise NotImplementedError(
            "subclasses of BaseAuthTokenMiddleware "
            "must provide a get_user_instance(token_key) method")

    def get_scope_header_value(self, scope, header_name):
        if isinstance(header_name, str):
            header_name = header_name.encode()
        elif not isinstance(header_name, bytes):
            raise ValueError("Header name must be string or bytes")

        headers = dict(scope["headers"])
        value = headers.get(header_name, headers.get(header_name.lower()))

        if not value:
            return None
        return value.decode()


class HeaderAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Base middleware which parses token key from request header."""

    header_name = None
    keyword = None

    def __init__(self, *args, header_name=None, keyword=None, **kwargs):
        self.header_name = str(header_name or self.header_name)
        self.keyword = str(keyword or self.keyword)

        super().__init__(*args, **kwargs)

    def get_token_key_string(self, scope):
        return self.get_scope_header_value(scope, self.header_name)

    @property
    def token_key_string_regex(self):
        """
        Regex to parse token key from token key string.
        Token key need to be in first group.
        """

        return rf"{self.keyword} ({self.token_regex})"