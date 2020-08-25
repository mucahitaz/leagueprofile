import os
import secrets
import requests
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import SummonerSearchForm
from app.models import Summoner
#from flask_login import login_user, current_user, logout_user, login_required


@app.route('/' , methods=['GET', 'POST'])
def home():
	form = SummonerSearchForm()
	if request.method == 'POST':
		req = request.form
		summoner_name = req["summoner_name"]
		server_name = req["server"]
		summoner = Summoner(name=form.summoner_name.data, server=form.server.data)
		db.session.add(summoner)
		db.session.commit()
		return redirect(url_for('profile',profile_id = summoner.id))
	return render_template('home.html',form=form)

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
	summoner = Summoner.query.get_or_404(profile_id)
	url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
	server_name = 'TR1'
	api_key = 'YOUR API KEY' #load this from an external file 
	r = requests.get(url.format(server_name,summoner.name,api_key)).json()
	summonerx = {
                'summoner_name' : r['name'],
                'level': r['summonerLevel'],
                'icon': r['profileIconId']
           }
	print(summonerx)
	return render_template('profile.html',post=summonerx)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         new_summoner = request.form.get('summoner')
		
#         if new_summoner:
#             new_summoner_obj = Summoner(name=new_summoner)
#             db.session.add(new_summoner_obj)
#             db.session.commit()

#     summoners = Summoner.query.all()


#     url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"

#     summoner_data = []

#     server_name = 'TR1'
#     api_key = 'YOUR API KEY '

#     for x in summoners:

#         r = requests.get(url.format(server_name,x.name,api_key)).json()

#         summoner = {
#                'summoner_name' : r['name'],
#                'level': r['summonerLevel'],
#                'icon': r['profileIconId']
#           }

#         summoner_data.append(summoner)
#         print(summoner_data)

#     return render_template('weather.html',summoner_data=summoner_data)
