from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import praw
import nltk
from getkey import getkey, key
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.download('vader_lexicon')

#main functions

def get_thread_info(subreddit, param):
    data = []

    for submission in reddit.subreddit(subreddit).search(param):
        data.add(submission.subreddit)
        data.add(submission.author_flair_text)
        data.add(submission.title)
        data.add(submission.shortlink)
        data.add(submission.id)
        data.add(submission.author)
        data.add(submission.num_comments)
        data.add(submission.upvote_ratio)  # percentage of upvotes from all votes
        data.add(submission.created_utc)

    df = pd.DataFrame(data, columns=['subreddit', 'flair', 'title', 'shortlink',
                                     'id', 'author', 'num_comments', 'upvote_ratio',
                                     'created_utc'])

    return df

def sentiment_analysis(dataframe):
    sia = SIA()
    results = []

    for line in dataframe['title']:
        pol_score = sia.polarity_scores(line)  # returns dict
        pol_score['text'] = line  # store line as headline key in dict
        results.append(pol_score)

    df = pd.DataFrame.from_records(results)

    dataframe['label'] = 0

    for n in df['compound']:
        if n < -0.5:
            dataframe['label'] = -2
        elif -0.5 <= n < 0:
            dataframe['label'] = -1
        elif 0 < n <= 0.5:
            dataframe['label'] = 1
        elif n > 0.5:
            dataframe['label'] = 2
        else:
            dataframe['label'] = 0

    return dataframe

#instructions - how to create Reddit app

print('''
전략개발팀 use ONLY!!! by Kirby

**SET UP - Reddit**
1. Log on to Reddit: https://www.reddit.com/
2. Create an app here: https://reddit.com/prefs/apps
(if it won't open, try this https://old.reddit.com/prefs/apps/) 
3. Select 'script'.
4. Set 'redirect uri' to: http://localhost:8888
5. Set name to whatever you want.
!!!LEAVE 'about url' & 'description' BLANK!!!
6. Click 'create app'. 
7. You're done! (Don't close the window pls)
''')

input('press the ENTER key to continue: ')

#set up for praw

agent_input = input('enter Reddit username (next to "developers"): ')
id_input = input('enter client_id (below "personal use script": ')
secret_input = input('enter client_secret (next to "secret"): ')

user_agent = f"PlsNoBlockMeReddit 1.0 by /u/{agent_input}"
reddit = praw.Reddit(
    client_id=id_input,
    client_secret=secret_input,
    user_agent=user_agent
)

print(f'''
Your script ID(?) for Reddit:
* user agent: {user_agent}
* client id: {id_input}
* client secret: {secret_input}
''')

input('press the ENTER key to continue: ')

print('''
**COMMANDS**
threads - scrapes + analyzes sentiment of headlines in a subreddit. (w/ search words)
comments - scrapes + analyzes sentiment of comments in a thread.
''')

user_input_command = input('Type a command: ')

'''
if user_input_command != None:
    #for Reddit threads
    if user_input_command == "threads":






    #for Reddit comments
    elif user_input_command == "comments":

    #for invalid command inputs
    else:
        input("Invalid command. Type a command: ")
'''
def get_thread_titles(subreddit, flair):
    data = set()
    for submission in reddit.subreddit(subreddit).search(flair):
        data.add(submission.title)
    return data

if user_input_command == "1":
    get_thread_titles("Genshin_Impact", "flair:Discussion")