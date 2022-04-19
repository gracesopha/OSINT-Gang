#This program allows for scraping details from the Reddit API directly using 
#Reddit API credentials stored in a local auth.yaml file.
#Results are returned to a CSV file
import yaml
import praw
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.download('vader_lexicon')

REDDIT_CONFIG_FILE = 'auth.yaml'

with open(REDDIT_CONFIG_FILE, 'r') as config_file:
  config = yaml.safe_load(config_file)
  redditId = config['reddit']['id']
  redditSecret = config['reddit']['secret']

reddit_read_only = praw.Reddit(client_id=redditId,      
                               client_secret=redditSecret,      
                               user_agent="windows:ITMS548-OSINT:v.9 (by u/CampaignSpiritual333")
#Create dictionary to hold values
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
                "body":[], \
                "sentimentPos":[], \
                "sentimentNeg":[], \
                "sentimentNeu":[], \
                "sentimentComp":[]}


#Set variables 
searchTerm = (input("Search Term to query:"))
resultSize = 500
allSubs = reddit_read_only.subreddit("all")
specQuery = (input("Customize the Query? Yes/No: "))

#If loop for customized queries
if (specQuery == "y" or specQuery == "Y" or specQuery == "yes" or specQuery == "Yes"):
  subName = reddit_read_only.subreddit((input("Name of the specific Subreddit: ")))
  resultSize = (eval(input("Number of results (Default: 500): ")))
  
  #For loop to iterate through search results based on user input
  for c in subName.search(searchTerm, limit=resultSize):
    
    #Append results to the dictionary
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
    topics_dict["sentimentPos"].append("")
    topics_dict["sentimentNeg"].append("")
    topics_dict["sentimentNeu"].append("")
    topics_dict["sentimentComp"].append("")

    #Creates a "sub" object for the current comment to scrape all replies
    sub = reddit_read_only.submission(id=c.id)
    sub.comments.replace_more(limit=None)
    
    #For loop to iterate through replies to the previous comment
    for i in sub.comments.list():
      #Calculate Sentiment
      sia = SIA()
      polarityScore= sia.polarity_scores(i.body)

      #Append to Dictionary
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
      topics_dict["sentimentPos"].append(polarityScore['pos'])
      topics_dict["sentimentNeg"].append(polarityScore['neg'])
      topics_dict["sentimentNeu"].append(polarityScore['neu'])
      topics_dict["sentimentComp"].append(polarityScore['compound'])

else:
  
  #For loop to iterate through search results based on default of 500 results and all subreddits
  for c in allSubs.search(searchTerm, limit=500):

    #Append results to the dictionary
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
    topics_dict["sentimentPos"].append("")
    topics_dict["sentimentNeg"].append("")
    topics_dict["sentimentNeu"].append("")
    topics_dict["sentimentComp"].append("")

    #Creates a "sub" object for the current comment to scrape all replies
    sub = reddit_read_only.submission(id=c.id)
    sub.comments.replace_more(limit=None)

    #For loop to iterate through replies to the previous comment
    for i in sub.comments.list():
      #Calculate Sentiment
      sia = SIA()
      polarityScore= sia.polarity_scores(i.body)
      
      #Append to Dictionary
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

#Writes the dictionary to a DataFrame
df = pd.DataFrame(topics_dict)

#Creates a CSV file, opens it, and outputs to it
f = open("reddit.csv", "a", encoding='utf-8')
f.write(df.to_csv())
f.close