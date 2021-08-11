-- Create the database called reddit_posts 
CREATE DATABASE reddit_posts;

-- Select reddit_posts database
USE reddit_posts;

-- Create table 
CREATE TABLE reddit_dataset(id INT AUTO_INCREMENT,
                            title MEDIUMTEXT,
                            subreddit VARCHAR(255),
                            PRIMARY KEY(id));