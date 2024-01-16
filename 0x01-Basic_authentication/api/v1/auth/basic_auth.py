#!/usr/bin/env python3
''' basic authentication file'''
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    ''' Basic Auth class '''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        ''' extract base64 authorization header'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[-1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        ''' decodes base64 string'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            d = base64.b64decode(base64_authorization_header).decode('utf-8')
            return d
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        ''' returns the user email and password from the Base64 decoded value.
        '''
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        ''' returns a user object
        '''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for i in users:
                if i.is_valid_password(user_pwd):
                    return i
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        retrieves a user instance of a request
        '''
        Auth_header = self.authorization_header(request)
        if Auth_header is None:
            return
        token = self.extract_base64_authorization_header(Auth_header)
        if token is None:
            return
        decoded = self.decode_base64_authorization_header(token)
        if decoded is None:
            return
        email, password = self.extract_user_credentials(decoded)
        if email is None and password is None:
            return
        return self.user_object_from_credentials(email, password)
