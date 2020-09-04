import requests
import json

def mastery_score_calculator(server_name,summoner_id,api_key):
	url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}"
	summoner_mastery_record = requests.get(url.format(server_name,summoner_id,api_key)).json()
	mastery_list_points = []
	for x in range(len(summoner_mastery_record)):
		a = (summoner_mastery_record[x]['championPoints'])
		mastery_list_points.append(a)
	return mastery_list_points

def mastery_champion_calculator(server_name,summoner_id,api_key):
	url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}"
	summoner_mastery_record = requests.get(url.format(server_name,summoner_id,api_key)).json()
	mastery_list_champs = []
	for x in range(len(summoner_mastery_record)):
		c = (summoner_mastery_record[x]['championId'])
		mastery_list_champs.append(c)
	return mastery_list_champs

def ddragon_champion_dictionary():
	json_data_hero = requests.get(
                "http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion.json").json()
	hero_id_name = {}
	for x in json_data_hero['data']:
		a = (json_data_hero['data'][x]['key'])
		b = (json_data_hero['data'][x]['id'])
		hero_id_name[a] = b
	return hero_id_name

def champion_mastery_score_zipper(mastery_champions,hero_id_name,mastery_scores):
	picked_champs = []
	champs_points = {}
	for x in mastery_champions:
			if str(x) in hero_id_name.keys():
				active_heroes = hero_id_name.get(str(x))
				picked_champs.append(active_heroes)
	for x in range(len(mastery_champions)):
		champs_points[picked_champs[x]] = mastery_scores[x]
#		champs_levels[picked_champs[x]] = mastery_list_levels[x]
	return champs_points