import os
import secrets
import requests
from flask import render_template, url_for, flash, redirect, request,session
from app import app, db
from app.forms import SummonerSearchForm
from app.models import Summoner
import json
from app.functions import mastery_score_calculator,mastery_champion_calculator,ddragon_champion_dictionary,champion_mastery_score_zipper
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
	mastery_scores = mastery_score_calculator(server_name=server_name,summoner_id=summoner['id'],api_key=API_KEY)
	mastery_champions = mastery_champion_calculator(server_name=server_name,summoner_id=summoner['id'],api_key=API_KEY)
	hero_id_name = ddragon_champion_dictionary()
	champs_points = champion_mastery_score_zipper(mastery_champions=mastery_champions,hero_id_name=hero_id_name,mastery_scores=mastery_scores)
	
	champion_names_for_graph = []
	champion_points_for_graph=[] 

	for key in champs_points.keys(): 
		champion_names_for_graph.append(key) 
	for value in champs_points.values(): 
		champion_points_for_graph.append(value) 
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Champion', "data": champion_points_for_graph[0:9]}]
	title = {"text": 'Top 10 Champions'}
	xAxis = {"categories": champion_names_for_graph[0:9]}
	yAxis = {"title": {"text": 'Point'}}
	return render_template('profile.html',post=summoner,champion=champs_points, chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
