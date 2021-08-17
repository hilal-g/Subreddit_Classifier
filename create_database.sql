-- Create the database called reddit_posts 
CREATE DATABASE reddit_posts;

-- Select reddit_posts database
USE reddit_posts;

-- Create table 
CREATE TABLE reddit_titles(id INT AUTO_INCREMENT,
                            title MEDIUMTEXT,
                            subreddit VARCHAR(255),
                            PRIMARY KEY(id));

-- Create table 
CREATE TABLE reddit_topics(id INT AUTO_INCREMENT,
                            title MEDIUMTEXT,
                            topic VARCHAR(255),
                            PRIMARY KEY(id));