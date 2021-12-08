import inspect

from bottle import request, PluginError, Bottle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm_base import Base


class SQLAlchemyPluginError(PluginError):
    pass


class SQLAlchemyPlugin:
    name = "SQLAlchemy Plugin"
    api = 2

    def __init__(self, keyword="db_session"):
        self.session = None
        self.keyword = keyword

    def setup(self, app: Bottle):
        for plugin in app.plugins:
            if isinstance(plugin, SQLAlchemyPlugin):
                if plugin.keyword == self.keyword:
                    raise PluginError("There is already a SQLAlchemy plugin installed.")
        engine = create_engine("sqlite:///database.sqlite")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def apply(self, callback, context):
        parameters = inspect.signature(callback).parameters
        if self.keyword not in parameters:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = self.session
            return callback(*args, **kwargs)

        return wrapper
