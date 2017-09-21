from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.odbc import User


class LoginView(MethodView):

    def post(self):
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if(user and user.password_is_valid(request.data['password'])):
                access_token = user.generate_token(user.id)
                if(access_token):
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200

            else:
                reponse = {
                    'message': 'Invalid email or password. Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

class RegistrationView(MethodView):
    """This class registers a new user"""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/register"""

        user = User.query.filter_by(email=request.data['email']).first()

        if(not user):
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }

                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response))
        else:
            response = {
                'message': 'User already exists. Please login.'
            }
            return make_response(jsonify(response)), 202

login_view = LoginView.as_view('login_view')
registration_view = RegistrationView.as_view('register_view')

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
