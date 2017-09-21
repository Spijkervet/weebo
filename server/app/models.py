from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

class User(db.Model):
    """User table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    '''
    alarms = db.relationship(
        'Alarm', order_by='Alarm.id', cascade="all, delete-orphan", backref='users'
    )
    '''

    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()


    def password_is_valid(self, password):
        """
        Checks the password against the hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)


    def save(self):
        """
        Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
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

    @staticmethod
    def get_all():
        return Alarm.query.filter_by(created_by=user_id) #Alarm.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Weebo: {}>".format(self.name)
