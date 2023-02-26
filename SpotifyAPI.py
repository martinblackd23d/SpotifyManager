#spotify API interface
#import WebAPIAccessTool as api
from calendar import c
from email.policy import default
from re import T
import secrets
import base64
#import http
#print(http.server)
from http.server import BaseHTTPRequestHandler, HTTPServer
import httphandler
import requests
import json
import time

user_id = ''

client_id = ''
client_secret = ''

base = 'https://api.spotify.com/v1'
redirect_uri = 'http://localhost:8888/callback'

#state = secrets.token_hex(16)
state = ''
code = ''
#print(api.GET(base, raw = True).content)

#def callback(params):
#	print(params)
#	server.server_close()

path = ''

token = ''

def generate_query(query):
	processed = []
	for key in query:
		processed.append(key + '=' + query[key])
	return '&'.join(processed)

def request_authorization():
	response_type = 'code'
	scope_array = ['user-modify-playback-state',
				'user-read-recently-played',
				'playlist-read-collaborative',
				'user-read-playback-state',
				'playlist-modify-public',
				'user-library-modify',
				'user-read-currently-playing',
				'user-library-read',
				'playlist-read-private',
				'playlist-modify-private']
	scope = '+'.join(scope_array)
	query = {
		'response_type': response_type,
		'client_id': client_id,
		'scope': scope,
		'redirect_uri': redirect_uri,
		'state': state
		}
	print(f'https://accounts.spotify.com/authorize?{generate_query(query)}')

def request_access_token():
	url = 'https://accounts.spotify.com/api/token'
	headers = {'Authorization': b'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')), 'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
	answer = requests.post(url, headers = headers, data = body).json()
	print(answer)
	token = answer['access_token']
	return token
	

#request_authorization()
#request_access_token()

def getplaylists(offset):
	url = f'{base}/users/{user_id}/playlists?limit=50&offset={offset}'
	headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
	body = ''
	print(token)
	response = requests.get(url, headers = headers, data = body).json()
	#print(response)
	#with open('D:\\playlists.json', 'w', encoding = 'utf-8') as f:
	#	f.write(response)
	return response


def getlikedsongs(i):
	#for i in range(20):
		#url = f'{base}/me/tracks?limit=50&offset={i*50}'
		url = f'{base}/me/tracks?limit=50&offset={i*50}'
		headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
		body = ''
		response = requests.get(url, headers = headers, data = body).text
		#with open(f'.\\likedsongs{i}.json', 'w', encoding = 'utf-8') as f:
		with open(f'.\\likedsongs.json', 'w', encoding = 'utf-8') as f:
			f.write(response)

def createplaylist(name):
	url = f'{base}/users/{user_id}/playlists?limit=50&offset=0'
	headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
	body = json.dumps({'name': name, 'public': False})
	response = requests.post(url, headers = headers, data = body).json()
	#print(response)
	return response['id']

def add_tracks(playlist_id, tries, songs):
	if tries > 10:
		print('limit reached')
		return True
	tracks = []
	#with open('./likedsongs.json', encoding = 'utf-8') as f:
	#	j = json.load(f)
	#for t in j['items']:
	#	tracks.append(t['track']['uri'])
	for i in songs:
		if i == None:
			continue
		tracks.append('spotify:track:'+i)

	url = f'{base}/playlists/{playlist_id}/tracks'
	headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
	body = json.dumps({'uris': tracks})
	response = requests.post(url, headers = headers, data = body)
	#print(response)
	if response.status_code < 300:
		return False
	print(response.text)
	if response.json()['error']['message'] == 'No tracks specified.':
		return True
	time.sleep(0.1)
	return add_tracks(playlist_id, tries + 1)


#getplaylists()
def copylikedtoplaylist():
	playlist_id = createplaylist()
	for i in range(20):
		getlikedsongs(i)
		if add_tracks(playlist_id, 0):
			print('finished')
			break
		time.sleep(0.1)


def getplaylistitems(idp):
	url = f'{base}/playlists/{idp}/tracks?limit=50&offset=0'
	headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
	body = ''
	response = requests.get(url, headers = headers, data = body).json()
	total = response['total']
	#with open('D:\\items.json', 'w', encoding = 'utf-8') as f:
	#	f.write(response)

	count = total // 50 + 1
	items = []
	for i in range(count):
		url = f'{base}/playlists/{idp}/tracks?limit=50&offset={i*50}'
		response = requests.get(url, headers = headers, data = body).json()
		for j in response['items']:
			items.append(j['track']['id'])
	return items


def savedata():
	request_authorization()

	location = httphandler.listen()

	code = location.split('=')[1].split('&')
	token = request_access_token()

	#copylikedtoplaylist()
	output = {'custom': {}, 'default': []}

	for i in range(8):
		playlists = getplaylists(i*50)
		for j in playlists['items']:
			name = j['name']
			idp = j['id']
			if j['owner']['display_name'] != '31qtfu5sxdsnx7e4uw37d4ch6dhi':
				output['default'].append(idp)
			else:
				output['custom'][name] = getplaylistitems(idp)
	with open('D:\\output.json', 'w', encoding = 'utf-8') as f:
		json.dump(output, f, ensure_ascii=False)
	print('success')

#savedata()
request_authorization()

location = httphandler.listen()

code = location.split('=')[1].split('&')
token = request_access_token()

data = {}
with open('D:\\output.json', 'r', encoding = 'utf-8') as f:
	data = json.load(f)
def defaultplaylists():
	for i in data['default']:
		url = f'{base}/playlists/{i}/followers'
		headers = {'Authorization': f'Bearer {token}','Content-Type': 'application/json'}
		body = {'public': False}
		response = requests.put(url,body, headers = headers)
		if response.status_code != 200:
			print(i)
			print(response)
		#print(response.text)
	print('success')
#defaultplaylists()
def customplaylists():
	for i in ['Favorites', 'Best Of The Best']:
		try:
			idp = createplaylist(i)
		except Exception as e:
			print(e)
			print(i)
		try:
			temp = []
			count = len(data['custom'][i])//100+1
			for j in range(count):
				temp = data['custom'][i][100*j:100*j+100]
				add_tracks(idp, 10,temp)
		except Exception as e:
			print(e)
			print(i)
		#break
	print('success')
customplaylists()