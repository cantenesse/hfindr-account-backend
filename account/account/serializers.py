# coding: utf-8

from marshmallow import Schema


class AccountSchema(Schema):
    class Meta:
        fields = ("email", "first_name", "last_name", "birth_date", "password" )


account_schema = AccountSchema()
account_schemas = AccountSchema(many=True)