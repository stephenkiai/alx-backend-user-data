#!/usr/bin/env python3
'''Auth class'''
import os
from typing import List, TypeVar
from flask import request


class Auth:
    """
        Manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            -path
            -excluded path
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith("/"):
            path += "/"
        if path in excluded_paths:
            return False
        for e_path in excluded_paths:
            e_path = e_path.rstrip("*")
            if path.find(e_path) != -1:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        returns none
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ return none
        """
        return None

    def session_cookie(self, request=None):
        '''
        Returns a cookie value
        '''
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
