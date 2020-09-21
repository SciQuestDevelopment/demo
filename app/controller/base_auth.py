from abc import ABC, abstractmethod
from app.models import User
from app import db, app as flask_app
from sqlalchemy import exc


"""
input will be:
{
    "email": "xxx",
    "type": "password(captcha)",
    "password": "password or captcha",
}
"""
class BaseAuth(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def check_input(self, input):
        pass
    
    """
    should return:
    {
        "email":"xxx",
        "type": "the type",
        "password": "string which will be our password"
    }
    """
    @abstractmethod
    def process_input(self, input):
        pass

    # authenticate users
    def login_user(self, info):
        email, type, password = info["email"], info["type"], info["password"]
        u = User.query.filter_by(email=email).first()
        if not u:
            return False, 'email does not exist'

        if type == "password":
            result = User.query.filter_by(email=email, password=password).first()
        elif type == "captcha":
            ...
            # result =

        if result is None:
            return False, 'login failed, {} incorrect'.format(type)
        
        return True, 'login successfully'

    def signup_user(self, info):
        email, type, password = info["email"], info["type"], info["password"]
        if User.query.filter_by(email=email).first() is not None:
            return False, 'email already exists'

        u = User(email=email, password=password)

        try:
            db.session.add(u)
            db.session.commit()
            return True, None
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False, 'sign up failed, may caused by db error'
