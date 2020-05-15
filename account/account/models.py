# -*- coding: utf-8 -*-
"""Account models."""
import datetime as dt

from account.database import Column, Model, SurrogatePK, db
from account.extensions import bcrypt


class Account(SurrogatePK, Model):
    __tablename__ = 'ACCOUNT'
    email = Column(db.String(100), unique=True, nullable=False)
    first_name = Column(db.String(100), unique=True, nullable=False)
    last_name = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    birth_date = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    token: str = ''

    def __init__(self, email, first_name, last_name, birth_date, password=None):
        """Create instance."""
        db.Model.__init__(self, email=email, first_name=first_name, last_name=last_name,
                          birth_date=birth_date, password=password)

        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        print("sfd")
        return '<Account({email!r})>'.format(email=self.email)
