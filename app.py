import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///summoner.db'


db = SQLAlchemy(app)

class Summoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_summoner = request.form.get('summoner')
        
        if new_summoner:
            new_summoner_obj = Summoner(name=new_summoner)
            db.session.add(new_summoner_obj)
            db.session.commit()

    summoners = Summoner.query.all()


    url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"

    summoner_data = []

    server_name = 'TR1'
    api_key = 'RGAPI-b0f1ed3e-6030-4a2f-8a61-34deb2c239f4'

    for x in summoners:

        r = requests.get(url.format(server_name,x.name,api_key)).json()

        summoner = {
               'summoner_name' : r['name'],
               'level': r['summonerLevel'],
               'icon': r['profileIconId']
          }

        summoner_data.append(summoner)
        print(summoner_data)

    return render_template('weather.html',summoner_data=summoner_data)
