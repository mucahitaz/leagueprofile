from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import Summoner


class SummonerSearchForm(FlaskForm):
    summoner_name = StringField('Summoner Name', validators=[DataRequired()])
    server = SelectField(u'Server', choices=[('TR1', 'Turkey'), ('EUW1', 'Europe W'),
    	('EUN1', 'Europe NE'), ('NA1', 'North America'),
    	('JP1', 'Japan'), ('LA1', 'Latin America 1'),
    	('LA2', 'Latin America 2'), ('OC1', 'Oceania'), ('RU', 'Russia')])
    submit = SubmitField('Search')