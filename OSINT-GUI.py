#This program allows for scraping details from the Reddit API directly using 
#Reddit API credentials stored in a local auth.yaml file.
#Results are returned to a CSV file
# For sending GET requests from the API
import requests
#For reading credentials from yaml file
import yaml
# For dealing with json responses we receive from the API
import json
import praw
# For displaying the data after
import pandas as pd
import nltk
import datetime
import dateutil.parser
import unicodedata
import csv
#To add wait time between requests
import time
# For saving access tokens and for file management when creating and adding to the dataset
import os
import tkinter as tk
import hashlib
import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

#Sets up logging
logging.basicConfig(filename='reddit_app.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


#Downloads the required dictionaries for text analysis
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')

#Pulls the Reddit API Credentials
REDDIT_CONFIG_FILE = 'auth.yaml'

with open(REDDIT_CONFIG_FILE, 'r') as config_file:
  config = yaml.safe_load(config_file)
  redditId = config['reddit']['id']
  redditSecret = config['reddit']['secret']
  tokenvalue = config['twitter']['key']
  usrername = config
 
 
#Sets up the Reddit API connection
reddit_read_only = praw.Reddit(client_id=redditId,      
                               client_secret=redditSecret,      
                               user_agent="windows:ITMS548-OSINT:v.9 (by u/CampaignSpiritual333")

#Sets up the Twitter API connection
os.environ['TOKEN'] = tokenvalue

def auth():
    return os.getenv('TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    logging.debug('Twitter API Response Code: %s',str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

#Set language of tweets to be searched for. Default: English
keyword_lang = " lang:en"



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

# Generate root window
root = tk.Tk()
root.geometry("800x600")
root.resizable(False, False)
root.title('OSINT Application')

# initialize variables
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

#Handles the login functionality
def loginClicked():
    #Pulls users and password hashes from the credential file
    cred_filename = 'CredFile.txt'
    pwDF=pd.read_csv(cred_filename,header=None)
    userDict=dict(zip(pwDF[0].values,pwDF[1].values))
  
    #Loop to check if the user is in the file and if they have the correct password
    if (user.get() in userDict):
     
      #Hashes the input password
      pwHash = hashlib.sha512( str(password.get()).encode("utf-8") ).hexdigest()
      
      #Compares the hashed input against the user's password from the database
      if pwHash == userDict[user.get()]:
        #Log successful login
        logging.info('user - %s has successfully logged in', user.get()) 
        #Welcome and disclaimer messages
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
      
        #Clears the sign in window, packs the main app window
        signin.pack_forget()
        mainApp.pack(padx=160, pady=30, fill='x', expand=True)
      
      #Error on invalid password
      else: 
        logging.warning('user - %s submitted an invalid password attempt', user.get()) 
        msg = f'Invalid Username or Password'
        showinfo(
            title='Information',
            message=msg
        )
    
    #Error on invalid user    
    else:
      logging.warning('user - %s submitted an invalid username', user.get()) 
      msg = f'Invalid Username or Password'
      showinfo(
        title='Information',
        message=msg
      )

#Clears the main app window and creates the add new user window
def addNewUser():
  logging.info('user - %s has run the new user tool', user.get())
  mainApp.pack_forget()
  newUser.pack(padx=160, pady=30, fill='x', expand=True)

#Creates the new user from the input
def writeNewUser():
  #Verifies new username has been entered
  if len(newUsername.get()) == 0:
        msg3 = 'Username can\'t be empty'
        showerror(
            title='Error',
            message=msg3
        )
  else:
    #Verifies new password has been entered
    if len(newPassword.get()) == 0:
        msg3 = 'Password can\'t be empty'
        showerror(
            title='Error',
            message=msg3
        )
    else:    
      uName = newUsername.get()
      logging.warning('user - %s created a new user %s', user.get(), newUsername.get()) 

      #Hashes the input password and stores it in the database
      pWordHashed = hashlib.sha512( str(newPassword.get()).encode("utf-8") ).hexdigest()
      #Writes new user to file
      f = open("CredFile.txt", "a", encoding='utf-8')
      f.write(uName+','+pWordHashed+ "\n")
      f.close
      #Pop up to let people know it worked
      msg = f'New User {newUsername.get()} has been added'
      showinfo(
        title='Information',
        message=msg
      )
      newUser.pack_forget()
      mainApp.pack()
#Clears the main app screen or custom config screen, packs the reddit main screen      
def redditButtonCMD():
  logging.info('user - %s has run the reddit tool', user.get())
  mainApp.pack_forget()
  redditCustomConfig.pack_forget()
  newUser.pack_forget()
  redditApp.pack(padx=160, pady=30, fill='x', expand=True)

#Clears the main app screen, packs the twitter button
def twitterButtonCMD():
  logging.info('user - %s has run the twitter tool', user.get())
  mainApp.pack_forget()
  twitterApp.pack(padx=160, pady=30, fill='x', expand=True)
  
#Runs the Reddit default query  
def redditDefaultCMD():
  #Verifies a query was entered
  if len(searchInput.get()) == 0:
        msg3 = 'Query can\'t be empty'
        showerror(
            title='Error',
            message=msg3
        )
        logging.warning('user - %s  has attempted a blank default query', user.get())
  else:
    logging.info('user - %s ran a default reddit search for: %s', user.get(), searchTerm) 
    #Clears the Reddit main app
    redditApp.pack_forget()
    #Packs the Reddit Default screen
    redditDefaultApp.pack(padx=160, pady=30, fill='x', expand=True)
    redditDefaultLabel1 = ttk.Label(redditDefaultApp, text="Running now")
    redditDefaultLabel1.pack()
    redditDefaultLabel2 = ttk.Label(redditDefaultApp, text="This will take a while. You will receive a CSV with results when it is done.")
    redditDefaultLabel2.pack()
    searchTerm = searchInput.get()
    #Pops up warning
    msg = f'This will take a while. You will receive a CSV with results when it is done.'
    showinfo(
      title='Information',
      message=msg
    )
    logging.info('Starting default reddit search for %s', searchTerm) 
    #Searches all subreddits for the search term, iterates through 5000 of them
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

      #Creates a "sub" object for the current comment to scrape all replies
      sub = reddit_read_only.submission(id=c.id)
      sub.comments.replace_more(limit=None)

      #For loop to iterate through replies to the previous comment
      for i in sub.comments.list():
        #Calculate Sentiment
        sia = SIA()
        #Imports stop words
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
    
    #Pulls the dictionary into a dataframe for processing
    df = pd.DataFrame(topics_dict)
    #Opens the output file, appends the dataframe contents
    f = open("reddit.csv", "a", encoding='utf-8')
    f.write(df.to_csv())
    f.close
    logging.info('Ending default query for: %s', searchTerm) 
    #Clears the Reddit default query, repacks the main Reddit app
    redditDefaultApp.pack_forget()
    redditApp.pack()

def create_url(keyword, max_results = 10):

    search_url = "https://api.twitter.com/2/tweets/search/recent" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)

#Runs the Twitter search
def twitterCMD():
  if len(searchInput.get()) == 0:
      msg3 = 'Query can\'t be empty'
      showerror(
        title='Error',
        message=msg3
      )
      logging.warning('user - %s  has attempted a blank custom query', user.get())   
  else:
    #Inputs for tweets
    bearer_token = auth()
    headers = create_headers(bearer_token)
    keyword = searchInput.get()
    max_results = 100
    strResultSize = customResultSize.get()
    resultSize=int(strResultSize)
    #Total number of tweets we collected from the loop
    total_tweets = 0

    # Create file
    csvFile = open("twitter.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['author id', 'created_at', 'geo', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet','Positive_Score','Negative_Score','Neutral_Score','Compound_Score'])
    csvFile.close()
    msg = f'Scraping {resultSize} tweets\nThis might take a while, please be patient.'
    showinfo(
      title='Information',
      message=msg
      )

    for i in range(0,1):
        logging.info('user - %s has run a query for %s on Twitter', user.get(), keyword)
        # Inputs
        count = 0 # Counting tweets per time period
        max_count = resultSize # Max tweets per time period
        flag = True
        next_token = None

        # Check if flag is true
        while flag:
            # Check if max_count reached
            if count >= max_count:
                break
            url = create_url(keyword, max_results)
            json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
            result_count = json_response['meta']['result_count']

            if 'next_token' in json_response['meta']:
                # Save the token to use for next call
                next_token = json_response['meta']['next_token']
                if result_count is not None and result_count > 0 and next_token is not None:
                    append_to_csv(json_response, "twitter.csv")
                    count += result_count
                    total_tweets += result_count
            # If no next token exists
            else:
                if result_count is not None and result_count > 0:
                    append_to_csv(json_response, "twitter.csv")
                    count += result_count
                    total_tweets += result_count
                   # msg = f'# of Tweets added this pass:  {count} \n Total # of tweets added: {total_tweets}'
                   # showinfo(
                   #   title='Information',
                   #   message=msg
                   #)
                #Since this is the final request, turn flag to false to move to the next time period.
                flag = False
                next_token = None
            #time.sleep(5)
    logging.info('user - %s - query for %s on Twitter returned %s tweets', user.get(), keyword, total_tweets)
    msg = f'Total # of Tweets added:  {total_tweets}'
    showinfo(
      title='Information',
      message=msg
      )

#Loads the Reddit custom search config page
def redditCustomCfg():
  #Verifies a query was entered
  if len(searchInput.get()) == 0:
      msg3 = 'Query can\'t be empty'
      showerror(
        title='Error',
        message=msg3
      )
      logging.warning('user - %s  has attempted a blank custom query', user.get())   
  else:
    #Clears the main Reddit app, packs the custom configuration page
    redditApp.pack_forget()
    redditCustomConfig.pack(padx=160, pady=30, fill='x', expand=True)
    
#Runs the scrape with the options from the custom configuration    
def redditCustomCMD():
  if len(customSubs.get()) == 0:
    msg3 = 'Subreddit can\'t be empty'
    showerror(
      title='Error',
      message=msg3
    )
    logging.warning('user - %s  has attempted a blank custom query', user.get()) 
  else:
    #Converts variables to useable forms
    searchTerm = searchInput.get()
    subName = reddit_read_only.subreddit(customSubs.get())
    strResultSize = customResultSize.get()
    resultSize=int(strResultSize)
    #Warns the user
    msg = f'This will take a while. You will receive a CSV with results when it is done.'
    showinfo(
      title='Information',
      message=msg
    )
    logging.info('user - %s has run a custom query for %s on %s subreddit, requesting %s results', user.get(), searchTerm, subName, resultSize) 
    #For loop to iterate through search results based on user input
    logging.info('Custom search query has started for %s on %s subreddit, requesting %s results', searchTerm, subName, resultSize) 
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
    #Creates a dataframe and pulls in the dictionary for processing
    df = pd.DataFrame(topics_dict)
    #Opens the output file, appends the data, closes the file
    f = open("reddit.csv", "a", encoding='utf-8')
    f.write(df.to_csv())
    f.close
    logging.info('Custom search query has ended for %s on %s subreddit, requesting %s results', searchTerm, subName, resultSize) 
    #clears the custom config and repacks the main Reddit app
    redditCustomConfig.pack_forget()
    redditApp.pack()

#Clears the main Reddit app and packs the main app
def mainAppCMD():
  logging.info('user - %s has returned to the tool selection', user.get())
  redditApp.pack_forget()
  twitterApp.pack_forget()
  mainApp.pack(padx=160, pady=30, fill='x', expand=True)      

def append_to_csv(json_response, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:

        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 3. Geolocation
        if ('geo' in tweet):
            geo = tweet['geo']['place_id']
        else:
            geo = " "

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. source
        source = tweet['source']

        # 8. Tweet text
        text = tweet['text']

        # 8a. Calculate Sentiment
        sia = SIA()
        stopWords = set(stopwords.words('english'))
        wordTokenize = word_tokenize(text)
        filteredSentence = [w for w in wordTokenize if not w.lower() in stopWords]
        filteredSentence = []
        for w in wordTokenize:
          if w not in stopWords:
            filteredSentence.append(w)
        polarityScore= sia.polarity_scores( ' '.join(filteredSentence))
        posScore = polarityScore['pos']
        negScore = polarityScore['neg']
        neuScore = polarityScore['neu']
        compScore = polarityScore['compound']
        # Assemble all data in a list
        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source, text, posScore, negScore, neuScore, compScore]

        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()


# Creates and packs the sign in frame
signin = ttk.Frame(root)
signin.pack(padx=160, pady=30, fill='x', expand=True)
#Creates the username field and label
user_label = ttk.Label(signin, text="Username:")
user_label.pack(fill='x', expand=True)
user_entry = ttk.Entry(signin, textvariable=user)
user_entry.pack(fill='x', expand=True)
user_entry.focus()

#Creates and packs the password field
password_label = ttk.Label(signin, text="Password:")
password_label.pack(fill='x', expand=True)
password_entry = ttk.Entry(signin, textvariable=password, show="*")
password_entry.pack(fill='x', expand=True)

#Creates the login button
login_button = ttk.Button(signin, text="Login", command=loginClicked)
login_button.pack(fill='x', expand=True, pady=10)

#Creates and packs the main app
mainApp = ttk.Frame(root)
mainLabel = ttk.Label(mainApp, text="Please Choose your tools:")
mainLabel.pack(fill='x', expand=True, pady=10)
redditButton = ttk.Button(mainApp, text="Reddit",command=redditButtonCMD)
redditButton.pack(fill='x', expand=True, pady=10)
twitterButton = ttk.Button(mainApp, text="Twitter",command=twitterButtonCMD)
twitterButton.pack(fill='x', expand=True, pady=10)
newUserButton = ttk.Button(mainApp, text="Add New User", command=addNewUser)
newUserButton.pack(fill='x', expand=True, pady=10)

#Creates the Reddit Default query frame
redditDefaultApp = ttk.Frame(root)

#Creates the New User frame, creates the entry boxes and labels
newUser = ttk.Frame(root)

#Username label and entry box
newUserLabel1 = ttk.Label(newUser, text="Enter the new username:")
newUserLabel1.pack(fill='x', expand=True, pady=10)
newUserEntry1 = ttk.Entry(newUser, textvariable=newUsername)
newUserEntry1.pack(fill='x', expand=True, pady=10)
newUserEntry1.focus()

#Password label and entry box
newUserLabel2 = ttk.Label(newUser, text="Enter the new password:")
newUserLabel2.pack(fill='x', expand=True, pady=10)
newUserEntry2 = ttk.Entry(newUser, textvariable=newPassword, show="*")
newUserEntry2.pack(fill='x', expand=True, pady=10)

#Add button
newUserAddButton = ttk.Button(newUser, text="Add 'em",command=writeNewUser)
newUserAddButton.pack(fill='x', expand=True, pady=10)

#Back Button
redditButton = ttk.Button(newUser, text="Back",command=redditButtonCMD)
redditButton.pack(fill='x', expand=True, pady=10)

#Reddit Custom Frame
redditCustomConfig = ttk.Frame(root)

#Subreddit query box and label
redditCustomLabel1 = ttk.Label(redditCustomConfig, text="Please Enter the subreddit to search")
redditCustomLabel1.pack(fill='x', expand=True, pady=10)
redditCustomEntry1 = ttk.Entry(redditCustomConfig, textvariable=customSubs)
redditCustomEntry1.pack(fill='x', expand=True, pady=10)
redditCustomEntry1.focus()

#Submission count box and label
redditCustomLabel2 = ttk.Label(redditCustomConfig, text="Please Enter the number of submissions to return")
redditCustomLabel2.pack(fill='x', expand=True, pady=10)
redditCustomEntry2 = ttk.Entry(redditCustomConfig, textvariable=customResultSize)
redditCustomEntry2.pack(fill='x', expand=True, pady=10)

#Go button and label
redditCustomGo = ttk.Button(redditCustomConfig, text="Let's Do It", command=redditCustomCMD)
redditCustomGo.pack(fill='x', expand=True, pady=10)
redditButton = ttk.Button(redditCustomConfig, text="Back",command=redditButtonCMD)
redditButton.pack(fill='x', expand=True, pady=10)

#Reddit Landing Frame
redditApp = ttk.Frame(root)

#Twitter Landing Frame
twitterApp = ttk.Frame(root)
twitterLabel1 = ttk.Label(twitterApp, text="Please enter a search term and number of tweets to retreive.")
twitterLabel1.pack(fill='x', expand=True, pady=10)
twitterSearchEntry = ttk.Entry(twitterApp, textvariable=searchInput)
twitterSearchEntry.pack(fill='x', expand=True, pady=10)
twitterSearchEntry1 = ttk.Entry(twitterApp, textvariable=customResultSize)
twitterSearchEntry1.pack(fill='x', expand=True, pady=10)
twitterSearchEntry.focus()
twitterScrapeButton = ttk.Button(twitterApp, text="Scrape", command=twitterCMD)
twitterScrapeButton.pack(fill='x', expand=True, pady=10)
twitterBackButton = ttk.Button(twitterApp, text="Back",command=mainAppCMD)
twitterBackButton.pack(fill='x', expand=True, pady=10)

#Query box and label
redditLabel1 = ttk.Label(redditApp, text="Please enter a search term, then select default or custom parameters.")
redditLabel1.pack(fill='x', expand=True, pady=10)
redditSearchEntry = ttk.Entry(redditApp, textvariable=searchInput)
redditSearchEntry.pack(fill='x', expand=True, pady=10)
redditSearchEntry.focus()


#Default button and label
redditDefaultButton = ttk.Button(redditApp, text="Default", command=redditDefaultCMD)
redditDefaultButton.pack(fill='x', expand=True, pady=10)

#Custom button and label
redditCustomButton = ttk.Button(redditApp, text="Custom", command=redditCustomCfg)
redditCustomButton.pack(fill='x', expand=True, pady=10)

#Back button and label
mainAppButton = ttk.Button(redditApp, text="Back to Tool Select", command=mainAppCMD)
mainAppButton.pack(fill='x', expand=True, pady=10)

#Runs main loop
root.mainloop()