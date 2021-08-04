import json 
import pprint 
import requests 

response = requests.get("https://www.reddit.com/r/askreddit.json?limit=10", headers = {'User-agent': 'your bot 0.1'})
data = response.json()

pprint.pprint(data)