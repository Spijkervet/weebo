from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    query = StringField('query', validators=[DataRequired()])
    api = SelectField(
        'api',
        choices=[('apiai', 'API AI'), ('wolframalpha', 'Wolfram Alpha'), ('wikipedia', 'Wikipedia')]
    )
    whisper = BooleanField('whisper')
