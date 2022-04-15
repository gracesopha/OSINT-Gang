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


if (specQuery == "y" or specQuery == "Y" or specQuery == "yes" or specQuery == "Yes"):
  subName = reddit_read_only.subreddit((input("Name of the specific Subreddit: ")))
  resultSize = (eval(input("Number of results (Default: 500): ")))
  for c in subName.search(searchTerm, limit=resultSize):
    submission = reddit_read_only.submission(id=c.id)
    submission.comments.replace_more(limit=None)
    topics_dict["title"].append(c.title)
    topics_dict["author"].append(c.author)
    topics_dict["author_fullname"].append(c.author_fullname)
    topics_dict["score"].append(c.score)
    topics_dict["id"].append(c.id)
    topics_dict["url"].append(c.url)
    topics_dict["NumOfComments"].append(c.num_comments)
    topics_dict["created"].append(c.created)
    topics_dict["subreddit_name_prefixed"].append(c.subreddit_name_prefixed)
    topics_dict["permalink"].append(c.permalink)
    topics_dict["body"].append(c.selftext)
    for i in submission.comments.list():
      topics_dict["title"].append(c.title)
      topics_dict["author"].append(i.author)
      topics_dict["author_fullname"].append("")
      topics_dict["score"].append(i.score)
      topics_dict["id"].append(i.id)
      topics_dict["url"].append(c.url)
      topics_dict["NumOfComments"].append(c.num_comments)
      topics_dict["created"].append(i.created)
      topics_dict["subreddit_name_prefixed"].append(i.subreddit_name_prefixed)
      topics_dict["permalink"].append(i.permalink)
      topics_dict["body"].append(i.body)
else:
  for c in allSubs.search(searchTerm, limit=500):
    submission = reddit_read_only.submission(id=c.id)
    submission.comments.replace_more(limit=None)
    topics_dict["title"].append(c.title)
    topics_dict["author"].append(c.author)
    topics_dict["author_fullname"].append(c.author_fullname)
    topics_dict["score"].append(c.score)
    topics_dict["id"].append(c.id)
    topics_dict["url"].append(c.url)
    topics_dict["NumOfComments"].append(c.num_comments)
    topics_dict["created"].append(c.created)
    topics_dict["subreddit_name_prefixed"].append(c.subreddit_name_prefixed)
    topics_dict["permalink"].append(c.permalink)
    topics_dict["body"].append(c.selftext)
    for i in submission.comments.list():
      topics_dict["title"].append(c.title)
      topics_dict["author"].append(i.author)
      topics_dict["author_fullname"].append("")
      topics_dict["score"].append(i.score)
      topics_dict["id"].append(i.id)
      topics_dict["url"].append(c.url)
      topics_dict["NumOfComments"].append(c.num_comments)
      topics_dict["created"].append(i.created)
      topics_dict["subreddit_name_prefixed"].append(i.subreddit_name_prefixed)
      topics_dict["permalink"].append(i.permalink)
      topics_dict["body"].append(i.body)

df = pd.DataFrame(topics_dict)
f = open("reddit.csv", "w", encoding='utf-8')
f.write(df.to_csv())
f.close