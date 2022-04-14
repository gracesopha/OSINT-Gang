# ITMS548-OSINT
Python Based programs to scrape Reddit using PRAW or PushShift.

## Prerequisites
Requires Python 3
### redditAPI
Uses the official Reddit API
API Documentation: https://www.reddit.com/dev/api/  
PRAW Documentation: https://praw.readthedocs.io/en/stable/

Requires PRAW and PYYAML:

    pip install praw
    pip install pyyaml

Expects Reddit API details in an auth.yaml file in this format:

    reddit:
    id: *App ID*
    secret: *API SECRET*

### PushShift
Uses PushShift https://pushshift.io/  
API documentation: https://github.com/pushshift/api

Requires Requests and Tabulate:

    pip install requests
    pip install tabulate