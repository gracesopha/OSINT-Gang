# OSINT-Gang

open source intelligence project

---

## Prerequisites

Requires Python 3.9

---

### OSINT-GUI

Scrapes Twitter or Reddit bases on query, assesses content sentement and returns a CSV file with the results.

Twitter API Documentation: [Twitter API Docs](https://developer.twitter.com/en/docs)  
Reddit API Documentation: [Reddit API Docs](https://www.reddit.com/dev/api/)  
PRAW Documentation: [PRAW Docs](https://praw.readthedocs.io/en/stable/)

Requires NLTK, PRAW, PANDAS, and PYYAML:

    pip install nltk
    pip install praw
    pip install pandas
    pip install pyyaml

Expects API Credentials in an auth.yaml file in this format:

    reddit:
      id: *App ID*
      secret: *API SECRET*
    twitter:
      key: *KEY*

Expects username and password database to be in a CredFile.txt file in this format (one pair per line):

    username,*SHA512 Password Hash*
---
## Works referenced

The basis for the twitter portion was made using this [tutorial](https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a).

A list of all the available access points for the Twitter scraper can be found [here](https://developer.twitter.com/en/docs/api-reference-index).
