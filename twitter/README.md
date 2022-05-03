# OSINT Twitter Scraper

Using Python and the Twitter v2 API this script will scrape twitter posts using a given keyword from a selected date range within the last 7 days.

## Prerequisites

Requires the pandas library for python, and a bearer token from a twitter developer account.

    pip install pandas

The bearer token will be requested once the script is initiated within the CLI.

## Output

This script will output 100 tweets that were found using the given keyword. It will also filter the tweets to be of the set language (By default English). These tweets will be collected into a csv file.

## Credits

This was made by following this [tutorial](https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a).
