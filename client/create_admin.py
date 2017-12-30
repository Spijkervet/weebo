import sys
from getpass import getpass

from run import app
from app import bcrypt, db
from app.models import User


def get_email():
    print("Enter the admin account's email address: ")
    email = input()
    if "@" not in email:
        print("This is not a valid email address")
        return get_email()
    return email

def get_password():
    password = getpass()
    if(getpass("Password (verify): ") != password):
        print("The passwords don't match, please try again.")
        return get_password()
    return password

def main():
    with app.app_context():

        db.metadata.create_all(db.engine)

        if User.query.all():
            print("A user already exists! Create another? (y/n): ")
            create = input()
            if create == "n":
                return

        email = get_email()
        password = get_password()

        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        print("Added a new admin account: {}, with password {}.".format(email, "*"*len(password)))


if __name__ == '__main__':
    sys.exit(main())
