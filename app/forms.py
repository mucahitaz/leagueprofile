from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import Summoner


class SummonerSearchForm(FlaskForm):
    summoner_name = StringField('Summoner Name', validators=[DataRequired()])
    server = SelectField(u'Server', choices=[('tr', 'Turkey'), ('euw', 'Europe West')])
    submit = SubmitField('Search')