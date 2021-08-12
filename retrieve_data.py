import mysql.connector 
import re

# Get the username and password 

with open('../sc_auth.txt') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    line = re.sub("\n", "", line)
    lines[i] = line

username = lines[0]
password = lines[1]

mydb = mysql.connector.connect(
    user=username, 
    password=password, 
    db="reddit_posts"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM reddit_dataset;")

reddit_data = mycursor.fetchall()

for x in reddit_data:
    print(x)