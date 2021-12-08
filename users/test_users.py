import bcrypt
import pytest
from boddle import boddle
from marshmallow import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from orm_base import Base
from users.api import register
from users.models import User


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://")
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    yield session
    session.close()


def test_register_user_endpoint(db_session):
    post_params = {
        "username": "random_username",
        "password": "askdfjakjsdf",
        "email": "dospro@fake.com",
    }
    with boddle(json=post_params):
        result = register(db_session)
        expected = {
            "id": 1,
            "username": "random_username",
            "email": "dospro@fake.com",
        }
        assert result == expected


def test_register_saves_user(db_session):
    post_params = {
        "username": "random_username",
        "password": "askdfjakjsdf",
        "email": "dospro@fake.com",
    }
    with boddle(json=post_params):
        register(db_session)

    users = db_session.query(User).all()
    assert len(users) == 1
    user = users[0]
    assert user.username == post_params["username"]
    assert user.email == post_params["email"]


def test_register_password_is_hashed(db_session):
    post_params = {
        "username": "random_username",
        "password": "secret_password",
        "email": "dospro@fake.com",
    }
    with boddle(json=post_params):
        register(db_session)

    users = db_session.query(User).all()
    assert len(users) == 1
    user = users[0]
    assert bcrypt.checkpw(post_params["password"].encode(), user.password)


def test_register_empty_body(db_session):
    with boddle():
        with pytest.raises(ValidationError):
            register(db_session)


def test_register_invalid_json(db_session):
    with boddle(body="invalid_json"):
        with pytest.raises(ValidationError):
            register(db_session)


def test_register_missing_input(db_session):
    sample_user = {
        "username": "fake_user",
    }
    with boddle(json=sample_user):
        with pytest.raises(ValidationError):
            register(db_session)


def test_register_invalid_email(db_session):
    sample_user = {
        "username": "fake_user",
        "password": "secret_password",
        "email": "bademail"
    }
    with boddle(json=sample_user):
        with pytest.raises(ValidationError):
            register(db_session)


def test_register_duplicate_user(db_session):
    sample_user = {
        "username": "fake_user",
        "password": "secret_password",
        "email": "fake@fake.com"
    }
    with boddle(json=sample_user):
        with pytest.raises(IntegrityError):
            register(db_session)
            register(db_session)
