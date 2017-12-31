# import jwt
from datetime import datetime, timedelta

from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import db, bcrypt

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Queries(Base):
    __tablename__ = "queries"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(512))
    response = db.Column(db.String(512))
    type = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(Base):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def logout(self):
        self.authenticated = False
        db.session.commit()

    def generate_token(self, user_id):
        """Generate the API access token"""

        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get("SECRET"),#TODO
                algorithm="HS256"
            )
            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Auth header"""
        try:
            payload = jwt.decode(token, current_app.config.get("SECRET"))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class Alarm(db.Model):
    """ Alarm table """

    __tablename__ = "alarms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    alarm_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

Base.metadata.create_all(bind=engine)
