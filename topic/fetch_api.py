import mysql.connector 
import re
import requests 

from nltk import TweetTokenizer 
from nltk.tokenize.treebank import TreebankWordDetokenizer 

# Get the username and password 

with open('../../sc_auth.txt') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line = re.sub("\n", "", line)
    lines[i] = line

username = lines[0]
password = lines[1]

subreddit_names = {"science": "science", "askscience": "science", "biology": "science",
                   "physics": "science", "chemistry": "science",
                   "sports": "sports", "nba": "sports", "soccer": "sports",
                   "nfl": "sports", "baseball": "sports",
                   "parenting": "family", "justnomil": "family", "entitledparents": "family",
                   "insaneparents": "family", "childfree": "family",
                   "personalfinance": "finance", "CanadianInvestor": "finance", "investing": "finance",
                   "economics": "finance", "personalfinancecanada": "finance",}

titles = []

# Extract titles from chosen subreddits by calling api

def titles_api(subreddit_names, titles):

    for name in subreddit_names:
        subreddit_name = name
        response = requests.get("https://www.reddit.com/r/" + subreddit_name + ".json?limit=100", headers = {'User-agent': 'your bot 0.1'})

        data = response.json()

        sub_titles = []

        for i in data['data']['children']:
            title = i['data']['title'].lower()
            title = re.sub("[^a-zA-Z0-9?]", " ", title)
            title = TweetTokenizer().tokenize(title)
            clean_title = TreebankWordDetokenizer().detokenize(title)
            text = i['data']['selftext'].lower()
            text = re.sub("[^a-zA-Z0-9?]", " ", text)
            text = TweetTokenizer().tokenize(text)
            if len(title) < 20:
                full_text = TreebankWordDetokenizer().detokenize(title + text[:20-len(title)])
            else:
                full_text = clean_title
            sub_titles.append((full_text, subreddit_name, subreddit_names[subreddit_name]))

        sub_titles = sub_titles[2:]
        titles.extend(sub_titles)

    return titles

sql = "INSERT INTO reddit_topics (title, subreddit, topic) VALUES (%s, %s, %s)"
titles = titles_api(subreddit_names, titles)

mydb = mysql.connector.connect(
    user=username, 
    password=password, 
    db="reddit_posts"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE reddit_topics(id INT AUTO_INCREMENT," 
                    + " title MEDIUMTEXT,"
                    + " subreddit VARCHAR(255),"
                    + " topic VARCHAR(255),"
                    + " PRIMARY KEY(id));")

mycursor.executemany(sql, titles)
mydb.commit()