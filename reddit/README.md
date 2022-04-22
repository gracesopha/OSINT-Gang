# ITMS548-OSINT

Python Based programs to scrape Reddit using PRAW or PushShift.  
Either Program will retreive the requested information

---

## Prerequisites

Requires Python 3

---

### redditAPI

Uses the official Reddit API
API Documentation: [Reddit API Docs](https://www.reddit.com/dev/api/)  
PRAW Documentation: [PRAW Docs](https://praw.readthedocs.io/en/stable/)

Requires NLTK, PRAW, PANDAS, and PYYAML:

    pip install nltk
    pip install praw
    pip install pandas
    pip install pyyaml

Expects [Reddit API details](https://www.reddit.com/wiki/api) in an auth.yaml file in this format:

    reddit:
      id: *App ID*
      secret: *API SECRET*

---
### redditAPIGUI

Uses the official Reddit API
API Documentation: [Reddit API Docs](https://www.reddit.com/dev/api/)  
PRAW Documentation: [PRAW Docs](https://praw.readthedocs.io/en/stable/)

Requires CRYPTOGRAPHY, NLTK, PRAW, PANDAS, and PYYAML:

    pip install nltk
    pip install praw
    pip install pandas
    pip install pyyaml
    pip install cryptography

Expects [Reddit API details](https://www.reddit.com/wiki/api) in an auth.yaml file in this format:

    reddit:
      id: *App ID*
      secret: *API SECRET*

Expects username and password database to be in a CredFile.txt file in this format (one pair per line):

    username,*SHA512 Password Hash*
---


### PushShift

Uses [PushShift](https://pushshift.io/)  
[API documentation](https://github.com/pushshift/api) - No API Key Required

Requires Pandas, Requests, and Tabulate:

    pip install pandas
    pip install requests
    pip install tabulate
