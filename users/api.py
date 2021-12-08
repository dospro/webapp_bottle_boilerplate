from bottle import request

from users.schemas import RegisterUserSchema


def register(db_session):
    """
    Endpoint for registering a new user in the database

    Input is validated through a marshmallow schema
    Saves the user to the database and returns the
    user information

    This may raise a variety of exceptions which bottle should
    translate into http error codes.
    """
    schema = RegisterUserSchema()
    user = schema.load(request.json)
    db_session.add(user)
    db_session.commit()
    return schema.dump(user)
