#This program allows for scraping details from the Reddit API directly using 
#Reddit API credentials stored in a local auth.yaml file.
#Results are returned to a CSV file
from itertools import count
from msilib.schema import TextStyle
from re import subn
from turtle import textinput
from typing_extensions import IntVar
from unittest import result
import yaml
import praw
import pandas as pd
import nltk
import datetime
import ast
import tkinter as tk
from cryptography.fernet import Fernet
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tkinter import LEFT, Entry, StringVar, ttk
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

import hashlib
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')

REDDIT_CONFIG_FILE = 'auth.yaml'

with open(REDDIT_CONFIG_FILE, 'r') as config_file:
  config = yaml.safe_load(config_file)
  redditId = config['reddit']['id']
  redditSecret = config['reddit']['secret']
  usrername = config

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

# root window
root = tk.Tk()
root.geometry("800x600")
root.resizable(False, False)
root.title('OSINT Application')

# store email address and password
user = tk.StringVar()
password = tk.StringVar()
searchInput = tk.StringVar()
customResultSize = tk.IntVar()
customSubs = tk.StringVar()
newUsername = tk.StringVar()
newPassword = tk.StringVar()
allSubs = reddit_read_only.subreddit("all")
resultSize = 5000
subCount = 1
commentCount = 1


def loginClicked():
    cred_filename = 'CredFile.txt'
    pwDF=pd.read_csv(cred_filename,header=None)
    userDict=dict(zip(pwDF[0].values,pwDF[1].values))
  
    if (user.get() in userDict):
      pwHash = hashlib.sha512( str(password.get()).encode("utf-8") ).hexdigest()
      if pwHash == userDict[user.get()]:
        msg = f'Hello: {user.get()} Welcome to the OSINT App.'
        showinfo(
            title='Information',
            message=msg
        )
        msg2 = f'This will scrape Reddit or twitter. All access is logged, be responsible.'
        showinfo(
            title='Information',
            message=msg2
            
        )
        signin.pack_forget()
        mainApp.pack(padx=160, pady=30, fill='x', expand=True)
      else: 
        msg = f'Invalid Username or Password'
        showinfo(
            title='Information',
            message=msg
        )
    else:
      msg = f'Invalid Username or Password'
      showinfo(
        title='Information',
        message=msg
      )

def addNewUser():
  mainApp.pack_forget()
  newUser.pack(padx=160, pady=30, fill='x', expand=True)

def writeNewUser():
  uName = newUsername.get()
  pWordHashed = hashlib.sha512( str(newPassword.get()).encode("utf-8") ).hexdigest()
  f = open("CredFile.txt", "a", encoding='utf-8')
  f.write(uName+','+pWordHashed+ "\n")
  f.close
  msg = f'New User {newUsername.get()} has been added'
  showinfo(
    title='Information',
    message=msg
  )
  newUser.pack_forget()
  mainApp.pack()
def redditButtonCMD():
  mainApp.pack_forget()
  redditCustomConfig.pack_forget()
  redditApp.pack(padx=160, pady=30, fill='x', expand=True)
 
  
def redditDefaultCMD():
  if len(searchInput.get()) == 0:
        msg3 = 'Query can\'t be empty'
        showerror(
            title='Error',
            message=msg3
        )
  else:
    redditApp.pack_forget()
    redditDefaultApp.pack(padx=160, pady=30, fill='x', expand=True)
    redditDefaultLabel1 = ttk.Label(redditDefaultApp, text="Running now")
    redditDefaultLabel1.pack()
    redditDefaultLabel2 = ttk.Label(redditDefaultApp, text="This will take a while. You will receive a CSV with results when it is done.")
    redditDefaultLabel2.pack()
    searchTerm = searchInput.get()
    msg = f'This will take a while. You will receive a CSV with results when it is done.'
    showinfo(
      title='Information',
      message=msg
    )
    for c in allSubs.search(searchTerm, limit=5000):
      
      #Convert Submission Time to DateTime
      submissionTimeStamp=datetime.datetime.utcfromtimestamp(c.created).strftime('%Y-%m-%d %H:%M:%S')

      #Append results to the dictionary
      topics_dict["title"].append(c.title)
      topics_dict["author"].append(c.author)
      topics_dict["author_fullname"].append(c.author_fullname)
      topics_dict["score"].append(c.score)
      topics_dict["id"].append(c.id)
      topics_dict["url"].append(c.url)
      topics_dict["NumOfComments"].append(c.num_comments)
      topics_dict["created"].append(submissionTimeStamp)
      topics_dict["subreddit_name_prefixed"].append(c.subreddit_name_prefixed)
      topics_dict["permalink"].append(c.permalink)
      topics_dict["body"].append(c.selftext)
      topics_dict["sentimentPos"].append("")
      topics_dict["sentimentNeg"].append("")
      topics_dict["sentimentNeu"].append("")
      topics_dict["sentimentComp"].append("")

      #Uncomment the following two lines to watch the progress (for debugging - can be removed)
      #print("Submission # ", subCount, " completed")
      #subCount=subCount+1

      #Creates a "sub" object for the current comment to scrape all replies
      sub = reddit_read_only.submission(id=c.id)
      sub.comments.replace_more(limit=None)

      #For loop to iterate through replies to the previous comment
      for i in sub.comments.list():
        #Calculate Sentiment
        sia = SIA()
        stopWords = set(stopwords.words('english'))
        wordTokenize = word_tokenize(i.body)
        filteredSentence = [w for w in wordTokenize if not w.lower() in stopWords]
        filteredSentence = []
        for w in wordTokenize:
          if w not in stopWords:
            filteredSentence.append(w)
        polarityScore= sia.polarity_scores( ' '.join(filteredSentence))
            
        #Convert Comment Time to DateTime
        commentTimeStamp=datetime.datetime.utcfromtimestamp(i.created).strftime('%Y-%m-%d %H:%M:%S')
      
        #Append to Dictionary
        topics_dict["title"].append(c.title)
        topics_dict["author"].append(i.author)
        topics_dict["author_fullname"].append("")
        topics_dict["score"].append(i.score)
        topics_dict["id"].append(i.id)
        topics_dict["url"].append(c.url)
        topics_dict["NumOfComments"].append(c.num_comments)
        topics_dict["created"].append(commentTimeStamp)
        topics_dict["subreddit_name_prefixed"].append(i.subreddit_name_prefixed)
        topics_dict["permalink"].append(i.permalink)
        topics_dict["body"].append(i.body)
        topics_dict["sentimentPos"].append(polarityScore['pos'])
        topics_dict["sentimentNeg"].append(polarityScore['neg'])
        topics_dict["sentimentNeu"].append(polarityScore['neu'])
        topics_dict["sentimentComp"].append(polarityScore['compound']) 
    df = pd.DataFrame(topics_dict)
    f = open("reddit.csv", "a", encoding='utf-8')
    f.write(df.to_csv())
    f.close
    redditDefaultApp.pack_forget()
    redditApp.pack()

def redditCustomCfg():
  if len(searchInput.get()) == 0:
      msg3 = 'Query can\'t be empty'
      showerror(
        title='Error',
        message=msg3
      )
  else:
    redditApp.pack_forget()
    redditCustomConfig.pack(padx=160, pady=30, fill='x', expand=True)
    
def redditCustomCMD():
  searchTerm = searchInput.get()
  subName = reddit_read_only.subreddit(customSubs.get())
  strResultSize = customResultSize.get()
  resultSize=int(strResultSize)
  msg = f'This will take a while. You will receive a CSV with results when it is done.'
  showinfo(
    title='Information',
    message=msg
  )
  #For loop to iterate through search results based on user input
  for c in subName.search(searchTerm, limit=resultSize):
    #Convert Submission Time to DateTime
    submissionTimeStamp=datetime.datetime.utcfromtimestamp(c.created).strftime('%Y-%m-%d %H:%M:%S')

    #Append results to the dictionary
    topics_dict["title"].append(c.title)
    topics_dict["author"].append(c.author)
    topics_dict["author_fullname"].append(c.author_fullname)
    topics_dict["score"].append(c.score)
    topics_dict["id"].append(c.id)
    topics_dict["url"].append(c.url)
    topics_dict["NumOfComments"].append(c.num_comments)
    topics_dict["created"].append(submissionTimeStamp)
    topics_dict["subreddit_name_prefixed"].append(c.subreddit_name_prefixed)
    topics_dict["permalink"].append(c.permalink)
    topics_dict["body"].append(c.selftext)
    topics_dict["sentimentPos"].append("")
    topics_dict["sentimentNeg"].append("")
    topics_dict["sentimentNeu"].append("")
    topics_dict["sentimentComp"].append("")
    
    #Uncomment the following two lines to watch the progress (for debugging - can be removed)
    #print("Submission # ", subCount, " completed")
    #subCount=subCount+1
    
    #Creates a "sub" object for the current comment to scrape all replies
    sub = reddit_read_only.submission(id=c.id)
    sub.comments.replace_more(limit=None)
    
    #For loop to iterate through replies to the previous comment
    for i in sub.comments.list():
      print(i.id)
      #Calculate Sentiment
      sia = SIA()
      stopWords = set(stopwords.words('english'))
      wordTokenize = word_tokenize(i.body)
      filteredSentence = [w for w in wordTokenize if not w.lower() in stopWords]
      filteredSentence = []
      for w in wordTokenize:
        if w not in stopWords:
          filteredSentence.append(w)
      polarityScore= sia.polarity_scores( ' '.join(filteredSentence))
    
      #Convert Comment Time to DateTime
      commentTimeStamp=datetime.datetime.utcfromtimestamp(i.created).strftime('%Y-%m-%d %H:%M:%S')
    
      #Append to Dictionary
      topics_dict["title"].append(c.title)
      topics_dict["author"].append(i.author)
      topics_dict["author_fullname"].append("")
      topics_dict["score"].append(i.score)
      topics_dict["id"].append(i.id)
      topics_dict["url"].append(c.url)
      topics_dict["NumOfComments"].append(c.num_comments)
      topics_dict["created"].append(commentTimeStamp)
      topics_dict["subreddit_name_prefixed"].append(i.subreddit_name_prefixed)
      topics_dict["permalink"].append(i.permalink)
      topics_dict["body"].append(i.body)
      topics_dict["sentimentPos"].append(polarityScore['pos'])
      topics_dict["sentimentNeg"].append(polarityScore['neg'])
      topics_dict["sentimentNeu"].append(polarityScore['neu'])
      topics_dict["sentimentComp"].append(polarityScore['compound'])
  df = pd.DataFrame(topics_dict)
  f = open("reddit.csv", "a", encoding='utf-8')
  f.write(df.to_csv())
  f.close
  redditCustomConfig.pack_forget()
  redditApp.pack()

def mainAppCMD():
  redditApp.pack_forget()
  mainApp.pack(padx=160, pady=30, fill='x', expand=True)      

# Sign in frame
signin = ttk.Frame(root)
signin.pack(padx=160, pady=30, fill='x', expand=True)


# email
user_label = ttk.Label(signin, text="Username:")
user_label.pack(fill='x', expand=True)

user_entry = ttk.Entry(signin, textvariable=user)
user_entry.pack(fill='x', expand=True)
user_entry.focus()

# password
password_label = ttk.Label(signin, text="Password:")
password_label.pack(fill='x', expand=True)

password_entry = ttk.Entry(signin, textvariable=password, show="*")
password_entry.pack(fill='x', expand=True)

# login button
login_button = ttk.Button(signin, text="Login", command=loginClicked)
login_button.pack(fill='x', expand=True, pady=10)

#Main Frame
mainApp = ttk.Frame(root)
mainLabel = ttk.Label(mainApp, text="Please Choose your tools:")
mainLabel.pack(fill='x', expand=True, pady=10)
redditButton = ttk.Button(mainApp, text="Reddit",command=redditButtonCMD)
redditButton.pack(fill='x', expand=True, pady=10)
newUserButton = ttk.Button(mainApp, text="Add New User", command=addNewUser)
newUserButton.pack(fill='x', expand=True, pady=10)


redditDefaultApp = ttk.Frame(root)

#New User Frame
newUser = ttk.Frame(root)
newUserLabel1 = ttk.Label(newUser, text="Enter the new username:")
newUserLabel1.pack(fill='x', expand=True, pady=10)
newUserEntry1 = ttk.Entry(newUser, textvariable=newUsername)
newUserEntry1.pack(fill='x', expand=True, pady=10)
newUserLabel2 = ttk.Label(newUser, text="Enter the new password:")
newUserLabel2.pack(fill='x', expand=True, pady=10)
newUserEntry2 = ttk.Entry(newUser, textvariable=newPassword, show="*")
newUserEntry2.pack(fill='x', expand=True, pady=10)
newUserAddButton = ttk.Button(newUser, text="Add 'em",command=writeNewUser)
newUserAddButton.pack(fill='x', expand=True, pady=10)
redditButton = ttk.Button(newUser, text="Back",command=redditButtonCMD)
redditButton.pack(fill='x', expand=True, pady=10)

#Reddit Custom Frame
redditCustomConfig = ttk.Frame(root)
redditCustomLabel1 = ttk.Label(redditCustomConfig, text="Please Enter the subreddit to search")
redditCustomLabel1.pack(fill='x', expand=True, pady=10)
redditCustomEntry1 = ttk.Entry(redditCustomConfig, textvariable=customSubs)
redditCustomEntry1.pack(fill='x', expand=True, pady=10)
redditCustomLabel2 = ttk.Label(redditCustomConfig, text="Please Enter the number of submissions to return")
redditCustomLabel2.pack(fill='x', expand=True, pady=10)
redditCustomEntry2 = ttk.Entry(redditCustomConfig, textvariable=customResultSize)
redditCustomEntry2.pack(fill='x', expand=True, pady=10)
redditCustomGo = ttk.Button(redditCustomConfig, text="Let's Do It", command=redditCustomCMD)
redditCustomGo.pack(fill='x', expand=True, pady=10)
redditButton = ttk.Button(redditCustomConfig, text="Back",command=redditButtonCMD)
redditButton.pack(fill='x', expand=True, pady=10)

#Reddit Landing Frame
redditApp = ttk.Frame(root)
redditLabel1 = ttk.Label(redditApp, text="Please enter a search term, then select default or custom parameters.")
redditLabel1.pack(fill='x', expand=True, pady=10)
redditSearchEntry = ttk.Entry(redditApp, textvariable=searchInput)
redditSearchEntry.pack(fill='x', expand=True, pady=10)
redditDefaultButton = ttk.Button(redditApp, text="Default", command=redditDefaultCMD)
redditDefaultButton.pack(fill='x', expand=True, pady=10)
redditCustomButton = ttk.Button(redditApp, text="Custom", command=redditCustomCfg)
redditCustomButton.pack(fill='x', expand=True, pady=10)
mainAppButton = ttk.Button(redditApp, text="Back to Tool Select", command=mainAppCMD)
mainAppButton.pack(fill='x', expand=True, pady=10)


root.mainloop()









