#!/usr/bin/env python3
from models.base import Base
from sqlalchemy import Column, String

class UserSession(Base):
    """ UserSession class
    """
    __tablename__ = 'user_sessions'

    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)

    def __init__(self, *args: list, **kwargs: dict):
        """ Constructor method
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.session_id = kwargs.get('session_id', '')
