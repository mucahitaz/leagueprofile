import os
import secrets
import requests
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import SummonerSearchForm
from app.models import Summoner
#from flask_login import login_user, current_user, logout_user, login_required

API_KEY = (open(r"app/static/rgapi.txt", "r")).read()

@app.route('/' , methods=['GET', 'POST'])
def home():
	form = SummonerSearchForm()
	if request.method == 'POST':
		req = request.form
		summoner_name = req["summoner_name"]
		server_name = req["server"]
		summoner = Summoner(name=form.summoner_name.data, server=form.server.data)
		existing_record = Summoner.query.filter_by(name=form.summoner_name.data,server=form.server.data).first()
		if existing_record:
			return redirect(url_for('profile',profile_id = existing_record.id,server_route = existing_record.server,summoner_route = existing_record.name))
		else:
			db.session.add(summoner)
			db.session.commit()
			return redirect(url_for('profile',profile_id = summoner.id,server_route = summoner.server,summoner_route = summoner.name))
	return render_template('home.html',form=form)

@app.route('/profile/<int:profile_id>/<server_route>/<summoner_route>')
def profile(profile_id,server_route,summoner_route):
	summoner = Summoner.query.get_or_404(profile_id)
	url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
	server_name = summoner.server
	api_key = API_KEY 
	r = requests.get(url.format(server_name,summoner.name,api_key)).json()
	summonerx = {
                'summoner_name' : r['name'],
                'level': r['summonerLevel'],
                'icon': r['profileIconId']
           }
	return render_template('profile.html',post=summonerx)
