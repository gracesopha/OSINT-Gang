#Utilizes PushShift API to pull Reddit details and outputs to a CSV file
#PushShift Documentation: https://github.com/pushshift/api

import requests
import json
import pandas as pd

searchTerm = (input("Search Term to query:"))
resultSize = 500
specQuery = (input("Customize the Query? Yes/No: "))
if (specQuery == "y" or specQuery == "Y"):
    subName = (input("Name of the specific Subreddit: "))
    resultSize = (input("Number of results (Max 500): "))
    queryString='https://api.pushshift.io/reddit/search/comment/?q='+searchTerm+'&subreddit='+subName+'&sort=desc&sort_type=created_utc&size='+resultSize
elif (specQuery == "yes" or specQuery == "Yes"):
   subName = (input("Name of the specific Subreddit: "))
   resultSize = (input("Number of results (Max 500): "))
   queryString='https://api.pushshift.io/reddit/search/comment/?q='+searchTerm+'&subreddit='+subName+'&sort=desc&sort_type=created_utc&size='+resultSize
else:
  subName = ""
  queryString='https://api.pushshift.io/reddit/search/comment/?q='+searchTerm+'&sort=desc&sort_type=created_utc&size=500'

data = requests.get(queryString)
df = pd.DataFrame(data.json()['data'])
df.drop(['author_flair_background_color', 'author_flair_css_class',
       'author_flair_richtext', 'author_flair_template_id',
       'author_flair_text', 'author_flair_text_color', 'author_flair_type',
       'author_patreon_flair'], axis=1, inplace = True)

  # Uncomment the following line to print to stdout
  #print(df.to_csv())   

f = open("reddit.csv", "w", encoding='utf-8')
f.write(df.to_csv())
f.close
