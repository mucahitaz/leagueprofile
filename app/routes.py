import os
import secrets
import requests
from flask import render_template, url_for, flash, redirect, request,session
from app import app, db
from app.forms import SummonerSearchForm
from app.models import Summoner
import json
#from flask_login import login_user, current_user, logout_user, login_required

API_KEY = (open(r"app/static/rgapi.txt", "r")).read()

@app.route('/' , methods=['GET', 'POST'])
def home():
	form = SummonerSearchForm()
	if request.method == 'POST':
		req = request.form.to_dict()
		summoner_name = req["summoner_name"]
		server_name = req["server"]
		return redirect(url_for('profile',summoner_name=summoner_name,server_name=server_name))
	return render_template('home.html',form=form)

@app.route('/profile')
def profile():
	print(request.method)
	summoner_name = request.args.get('summoner_name')
	server_name = request.args.get('server_name')
	url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
	api_key = API_KEY 
	r = requests.get(url.format(server_name,summoner_name,api_key)).json()
	summoner = {
                'summoner_name' : r['name'],
                'level': r['summonerLevel'],
                'icon': r['profileIconId']
           }
	return render_template('profile.html',post=summoner)
