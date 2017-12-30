from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import db, bcrypt

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

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


    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

Base.metadata.create_all(bind=engine)
