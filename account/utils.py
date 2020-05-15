# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from account.account.models import Account  # noqa


def jwt_identity(payload):
    return Account.get_by_id(payload)


def identity_loader(account):
    return account.email
