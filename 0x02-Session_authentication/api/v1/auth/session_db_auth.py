#!/usr/bin/env python3
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4

class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """ Creates and stores a new instance of UserSession and returns the Session ID
        """
        if user_id is None:
            return None

        session_id = str(uuid4())
        new_session = UserSession(user_id=user_id, session_id=session_id)
        self._session.add(new_session)
        self._session.commit()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the User ID by requesting UserSession in the database based on session_id
        """
        if session_id is None:
            return None

        user_session = self._session.query(UserSession).filter_by(session_id=session_id).first()

        if user_session is None or self.session_duration <= 0:
            return None

        created_at = user_session.created_at
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID from the request cookie
        """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False

        user_session = self._session.query(UserSession).filter_by(session_id=session_cookie).first()
        if user_session is None:
            return False

        self._session.delete(user_session)
        self._session.commit()

        return True
