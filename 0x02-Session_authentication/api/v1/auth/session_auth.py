#!/usr/bin/env python3
''' SessionAuth class
'''
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    ''' creating a new authentication mechanism
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        creates a Session ID for a user_id
        '''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        s_id = str(uuid4())
        self.user_id_by_session_id[s_id] = user_id
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        returns a User ID based on a Session ID
        '''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''
        returns a User instance based on a cookie value
        '''
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        '''
        deletes the user session / logout:
        '''
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
