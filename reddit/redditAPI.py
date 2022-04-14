#This program allows for scraping details from the Reddit API directly using 
#Reddit API credentials stored in a local auth.yaml file.
#Results are returned to a CSV file
import yaml
import praw
import pandas as pd

REDDIT_CONFIG_FILE = 'auth.yaml'

with open(REDDIT_CONFIG_FILE, 'r') as config_file:
  config = yaml.safe_load(config_file)
  redditId = config['reddit']['id']
  redditSecret = config['reddit']['secret']

reddit_read_only = praw.Reddit(client_id=redditId,      
                               client_secret=redditSecret,      
                               user_agent="windows:ITMS548-OSINT:v.9 (by u/CampaignSpiritual333")

topics_dict = { "title":[], \
                "author":[], \
                "author_fullname":[], \
                "score":[], \
                "id":[], \
                "url":[], \
                "NumOfComments": [], \
                "created": [], \
                "subreddit_name_prefixed":[], \
                "permalink":[], \
                "body":[]}


searchTerm = (input("Search Term to query:"))
resultSize = 500
allSubs = reddit_read_only.subreddit("all")
specQuery = (input("Customize the Query? Yes/No: "))
if (specQuery == "y" or specQuery == "Y"):
  subName = reddit_read_only.subreddit((input("Name of the specific Subreddit: ")))
  resultSize = (eval(input("Number of results (Default: 500): ")))
  for i in subName.search(searchTerm, limit=resultSize):
    topics_dict["title"].append(i.title)
    topics_dict["author"].append(i.author)
    topics_dict["author_fullname"].append(i.author_fullname)
    topics_dict["score"].append(i.score)
    topics_dict["id"].append(i.id)
    topics_dict["url"].append(i.url)
    topics_dict["NumOfComments"].append(i.num_comments)
    topics_dict["created"].append(i.created)
    topics_dict["subreddit_name_prefixed"].append(i.subreddit_name_prefixed)
    topics_dict["permalink"].append(i.permalink)
    topics_dict["body"].append(i.selftext)
elif (specQuery == "yes" or specQuery == "Yes"):
  subName = reddit_read_only.subreddit((input("Name of the specific Subreddit: ")))
  resultSize = (eval(input("Number of results (Default: 500): ")))
  for i in subName.search(searchTerm, limit=resultSize):
    topics_dict["title"].append(i.title)
    topics_dict["author"].append(i.author)
    topics_dict["author_fullname"].append(i.author_fullname)
    topics_dict["score"].append(i.score)
    topics_dict["id"].append(i.id)
    topics_dict["url"].append(i.url)
    topics_dict["NumOfComments"].append(i.num_comments)
    topics_dict["created"].append(i.created)
    topics_dict["subreddit_name_prefixed"].append(i.subreddit_name_prefixed)
    topics_dict["permalink"].append(i.permalink)
    topics_dict["body"].append(i.selftext)
else:
  for i in allSubs.search(searchTerm, limit=500):
    topics_dict["title"].append(i.title)
    topics_dict["author"].append(i.author)
    topics_dict["author_fullname"].append(i.author_fullname)
    topics_dict["score"].append(i.score)
    topics_dict["id"].append(i.id)
    topics_dict["url"].append(i.url)
    topics_dict["NumOfComments"].append(i.num_comments)
    topics_dict["created"].append(i.created)
    topics_dict["subreddit_name_prefixed"].append(i.subreddit_name_prefixed)
    topics_dict["permalink"].append(i.permalink)
    topics_dict["body"].append(i.selftext)

df = pd.DataFrame(topics_dict)
f = open("reddit.csv", "w", encoding='utf-8')
f.write(df.to_csv())
f.close