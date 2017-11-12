from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    query = StringField('query', validators=[DataRequired()])
    whisper = BooleanField('whisper')
