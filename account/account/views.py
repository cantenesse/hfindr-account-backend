# -*- coding: utf-8 -*-
"""Account views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, create_access_token, current_user
from sqlalchemy.exc import IntegrityError
from account.database import db
from account.exceptions import InvalidUsage
from .models import Account
from .serializers import account_schema, account_schemas
blueprint = Blueprint('account', __name__)


@blueprint.route('/api/v1/account', methods=('POST',))
@use_kwargs(account_schema)
@marshal_with(account_schemas)
def register_user(email, first_name, last_name, birth_date, password):
    print("email: %s, password: %s" % (email, password))
    try:
        #account = Account(email, first_name, last_name, birth_date, password=password).save()
        account = Account(email, first_name, last_name, birth_date, password=password)
        account.save()
        account.user.token = create_access_token(identity={"email": email})
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.user_already_registered()
    #return account.email


@blueprint.route('/api/v1/account/login', methods=('POST',))
@jwt_optional
@use_kwargs(account_schema)
@marshal_with(account_schema)
def login_user(email, password, **kwargs):
    user = Account.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        user.token = create_access_token(identity=user, fresh=True)
        return user
    else:
        raise InvalidUsage.user_not_found()


@blueprint.route('/api/v1/account', methods=('GET',))
@jwt_required
@marshal_with(account_schema)
def get_user():
    user = current_user
    # Not sure about this
    user.token = request.headers.environ['HTTP_AUTHORIZATION'].split('Token ')[1]
    return current_user

