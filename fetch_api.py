import json 
import mysql.connector
import pprint 
import re
import requests 

from nltk import TweetTokenizer 
from nltk.tokenize.treebank import TreebankWordDetokenizer 

# Get the username and password 

with open('../sc_auth.txt') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line = re.sub("\n", "", line)
    lines[i] = line

username = lines[0]
password = lines[1]

# Extract titles from chosen subreddits 

subreddit_names = ["askhistorians",
                    "writingprompts",
                    "television",
                    "explainlikeimfive",
                    "lifeprotips",
                    "relationship_advice",
                    "science",
                    "books",
                    "nba",
                    "philosophy"]

titles = []

for i in subreddit_names:
    subreddit_name = i
    response = requests.get("https://www.reddit.com/r/" + subreddit_name + ".json?limit=100", headers = {'User-agent': 'your bot 0.1'})

    data = response.json()

    sub_titles = []

    for i in data['data']['children']:
        title = TweetTokenizer().tokenize(i['data']['title'])
        if 'selftext_html' in i['data']:
            text = i['data']['selftext_html']
        data = i['data']
        sub_titles.append((TreebankWordDetokenizer().detokenize(title), subreddit_name))

    sub_titles = sub_titles[2:]
    titles.extend(sub_titles)

sql = "INSERT INTO reddit_dataset (title, subreddit) VALUES (%s, %s)"

mydb = mysql.connector.connect(
    user=username, 
    password=password, 
    db="reddit_posts"
)

mycursor = mydb.cursor()

mycursor.executemany(sql, titles)
mydb.commit()
