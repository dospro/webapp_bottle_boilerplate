import bcrypt
from marshmallow import Schema, fields, post_load

from users.models import User


class RegisterUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Email(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        hashed_password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
        return User(
            username=data["username"],
            password=hashed_password,
            email=data["email"]
        )
