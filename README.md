# OSINT-Gang

open source intelligence project

---

## Prerequisites

Requires Python 3

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
