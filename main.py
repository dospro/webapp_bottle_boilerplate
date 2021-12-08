from bottle import route, run, install, request

from plugins.sqlalchemy import SQLAlchemyPlugin
from users.models import User


@route("/")
def index():
    for row in request.db_session.query(User).all():
        print(row.username)
    raise Exception("Error!")
    return "Hello world"


if __name__ == "__main__":
    install(SQLAlchemyPlugin())
    run(host="localhost", port=8080)
