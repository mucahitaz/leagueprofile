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
def profile(chartID = 'chart_ID', chart_type = 'column', chart_height = 500):
	summoner_name = request.args.get('summoner_name')
	server_name = request.args.get('server_name')
	url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}"
	api_key = API_KEY 
	r = requests.get(url.format(server_name,summoner_name,api_key)).json()
	if 'status' in r:
		return redirect(url_for('home'))
	summoner = {
	                'summoner_name' : r['name'],
	                'level': r['summonerLevel'],
	                'icon': r['profileIconId'],
	                'id':r['id']
	           }
	new_url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}"
	summoner_mastery_record = requests.get(new_url.format(server_name,summoner['id'],api_key)).json()
	mastery_list_champs = []
	mastery_list_points = []
	mastery_list_levels = []
	champs_points = {}
	picked_champs = []
	champs_levels = {}
	for x in range(len(summoner_mastery_record)):
		c = (summoner_mastery_record[x]['championId'])
		mastery_list_champs.append(c)
		a = (summoner_mastery_record[x]['championPoints'])
		mastery_list_points.append(a)
		b = (summoner_mastery_record[x]['championLevel'])
		mastery_list_levels.append(b)
	"""todo: rewrite this section as a function"""
	json_data_hero = requests.get(
                "http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json").json()
	hero_id_name = {}
	for x in json_data_hero['data']:
		a = (json_data_hero['data'][x]['key'])
		b = (json_data_hero['data'][x]['id'])
		hero_id_name[a] = b

	for x in mastery_list_champs:
			if str(x) in hero_id_name.keys():
				active_heroes = hero_id_name.get(str(x))
				picked_champs.append(active_heroes)

	for x in range(len(summoner_mastery_record)):
		champs_points[picked_champs[x]] = mastery_list_points[x]
		champs_levels[picked_champs[x]] = mastery_list_levels[x]
	q = []
	w=[] 
	for key in champs_points.keys(): 
		q.append(key) 
	for value in champs_points.values(): 
		w.append(value) 
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Champion', "data": w[0:9]}]
	title = {"text": 'Top 10 Champions'}
	xAxis = {"categories": q[0:9]}
	yAxis = {"title": {"text": 'Point'}}
	return render_template('profile.html',post=summoner,champion=champs_points, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
