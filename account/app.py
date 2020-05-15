# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from account.extensions import bcrypt, cache, db, jwt, cors

from account import commands, account
from account.settings import AccountConfig
from account.exceptions import InvalidUsage


def create_app(config_object=AccountConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
#    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    jwt.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(account.views.blueprint, origins=origins)

    app.register_blueprint(account.views.blueprint)


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'Account': account.models.Account,
        }

    app.shell_context_processor(shell_context)


#def register_commands(app):
#    """Register Click commands."""
#    app.cli.add_command(commands.test)
#    app.cli.add_command(commands.lint)
#    app.cli.add_command(commands.clean)
#    app.cli.add_command(commands.urls)

#!/usr/bin/env python3.7
from flask import Flask
from flask import request
import json
import sqlalchemy

#app = Flask(__name__)
#ROUTE_PREFIX = "/api/v1/account"
#
#
#def signup():
#    signup_data = json.loads(request.data)
#    return signup_data["account"]["email"]
#
#
#@app.route(ROUTE_PREFIX + "/signup", methods=["POST"])
#def login():
#    if request.method == "POST":
#        return signup()
#
#
#class DatabaseService:
#    def __init__(self, user, password, host, db):
#        self.user = user
#        self.host = host
#        self.password = password
#        self.db = db
#
#    def create_engine(self):
#        return sqlalchemy.create_engine(
#            "mysql+mysqlconnector://%s:%s@%s:3306/%s" % (self.user,
#                                                         self.password,
#                                                         self.host,
#                                                         self.db),
#            echo=True)
#
#
#class Account:
#    __tablename__ = "account"
#
#    email = sqlalchemy.Column(sqlalchemy.String(length=100), primary_key=True)
#    first_name = sqlalchemy.Column(sqlalchemy.String(length=100))
#    last_name = sqlalchemy.Column(sqlalchemy.String(length=100))
#    password = sqlalchemy.Column(sqlalchemy.String(length=129))
#    birth_date = sqlalchemy.Column(sqlalchemy.String(length=8))
#
#    def __repr__(self):
#        return "<Account(email='{0}', first_name='{0}'," \
#               "last_name='{0}', password='{0}', birth_date='{0}'>".format(
#                self.email, self.first_name, self.last_name, self.password, self.birth_date)
#
#
#
#
#
#if __name__ == '__main__':
#    database = DatabaseService("account", "hfindr", "localhost", "account")
#    engine = database.create_engine()
#    connection = engine.connect()
#    app.config["db_connection"] = connection
#    app.run()