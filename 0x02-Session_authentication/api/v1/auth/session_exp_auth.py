#!/usr/bin/env python3
''' SessionExpAuth class
'''
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv
from uuid import uuid4


class SessionExpAuth(SessionAuth):
    ''' creating a new authentication mechanism with session expiration
    '''

    def __init__(self):
        ''' Constructor method
        '''
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        '''
        creates a Session ID for a user_id with expiration date
        '''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''
        returns a User ID based on a Session ID with expiration date
        '''
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        if "created_at" not in session_dict:
            return None

        created_at = session_dict["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict.get("user_id")
