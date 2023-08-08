import pandas as pd
from IPython.display import display
import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from praw.models import MoreComments

nltk.download('vader_lexicon')

#main functions
def get_thread_info(subreddit, param, n=1000):
    data = []
    keys = ['subreddit', 'flair', 'title', 'shortlink',
            'id', 'author', 'num_comments', 'upvote_ratio', 'created_utc']

    for submission in reddit.subreddit(subreddit).search(param, limit=n):

        dicts = {}
        values = []

        values.append(submission.subreddit)
        values.append(submission.author_flair_text)
        values.append(submission.title)
        values.append(submission.shortlink)
        values.append(submission.id)
        values.append(submission.author)
        values.append(submission.num_comments)
        values.append(submission.upvote_ratio)  # percentage of upvotes from all votes
        values.append(submission.created_utc)

        for i in range(len(keys)):
            dicts[i] = values[i]

        data.append(dicts)

    df = pd.DataFrame.from_dict(data)
    df.rename(columns={0: 'subreddit', 1: 'flair', 2: 'title',
                       3: 'shortlink', 4: 'id', 5: 'author',
                       6: 'num_comments', 7: 'upvote_ratio',
                       8: 'created_utc'}, inplace=True)

    return df
def sentiment_analysis_threads(dataframe):
    sia = SIA()
    results = []

    for line in dataframe['title']:
        pol_score = sia.polarity_scores(line)  # returns dict
        pol_score['headline'] = line  # store line as headline key in dict
        results.append(pol_score)

    df = pd.DataFrame.from_records(results)

    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1  # positive
    df.loc[df['compound'] < -0.2, 'label'] = -1  # negative

    df2 = df[['headline', 'label']]

    dataframe.insert(9, 'sentiment', df2['label'])

    return dataframe
def sentiment_analysis_comments(dataframe):
    sia = SIA()
    results = []

    for line in dataframe['body']:
        pol_score = sia.polarity_scores(line)  # returns dict
        pol_score['headline'] = line  # store line as headline key in dict
        results.append(pol_score)

    df = pd.DataFrame.from_records(results)

    df['label'] = 0
    df.loc[df['compound'] > 0.2, 'label'] = 1  # positive
    df.loc[df['compound'] < -0.2, 'label'] = -1  # negative

    df2 = df[['headline', 'label']]

    dataframe.insert(8, 'sentiment', df2['label'])

    return dataframe
def get_comments(url):
    data = []
    keys = ['subreddit', 'submission_title', 'permalink', 'id',
            'author', 'body', 'score', 'created_utc']

    submission = reddit.submission(url=url)
    # submission.replace_more_comments(limit=None, threshold=0)

    for comment in submission.comments:

        if isinstance(comment, MoreComments):
            continue

        dicts = {}
        values = []

        values.append(submission.subreddit)
        values.append(submission.title)
        values.append(submission.shortlink)
        values.append(comment.id)
        values.append(comment.author)
        values.append(comment.body)
        values.append(comment.score)
        values.append(comment.created_utc)

        for i in range(len(keys)):
            dicts[i] = values[i]

        data.append(dicts)

    df = pd.DataFrame.from_dict(data)
    df.rename(columns={0: 'subreddit', 1: 'submission_title', 2: 'shortlink',
                       3: 'id', 4: 'author', 5: 'body',
                       6: 'score', 7: 'created_utc'}, inplace=True)

    return df

#instructions - how to create Reddit app

print('''
전략개발팀 use ONLY!!! by Kirby

#NOTE: Please read everything carefully + follow the instructions
    B/C the dev. does not know how to catch exceptions.
    And you'll have to rerun the program from the beginning if anything goes wrong.
    Sorry...

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

print('''
Please input the following:
(Make sure there are no spaces at the end!!!)
''')

agent_input = input('enter Reddit username (next to "developers"): ')
id_input = input('enter client_id (below "personal use script"): ')
secret_input = input('enter client_secret (next to "secret"): ')

user_agent = f"PracticeScript 1.1 by /u/{agent_input}"
reddit = praw.Reddit(
    client_id=id_input,
    client_secret=secret_input,
    user_agent=user_agent
)

print(f'''
Here's the ID of your Reddit script: 
* user agent: {user_agent}
* client id: {id_input}
* client secret: {secret_input}
''')


input('press the ENTER key to continue: ')

print('''
**COMMANDS**
/threads - scrapes + analyzes sentiment of headlines in a subreddit. (w/ search words)
/comments - scrapes + analyzes sentiment of comments in a thread.
''')

user_input_command = input('Type a command: ')

#for Reddit threads
if user_input_command == "/threads":

    print('''
    **ABOUT THREADS**
    This script takes one or more subreddits;
    Analyzes the sentiment of the titles (-1 / 0 / 1);
    Returns a .CSV file of the results.
        
    documentation: https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html
    ''')

    subreddit = input('Input subreddit(s) | ex) Genshin_Impact: ')
    param = input('Input search words | ex) flair:Discussion, flair:News: ')
    limit = input('Input # of threads (default = 1000) | ex) 100: ')

    df = get_thread_info(subreddit, param, int(limit))
    sentiment_analysis_threads(df)

    print('----------INFO-----------')

    print("Distribution (sentiment): ")
    display(df.sentiment.value_counts())

    print('-------------------------')

    print("Percent distribution (sentiment): ")
    display(df.sentiment.value_counts(normalize=True) * 100)

    print('-------------------------')

    user_response = input('Would you like to export as a .CSV file? (y/n): ')

    if user_response.lower() == 'y':
        file_name = input('Input file name | ex) genshin_threads.csv: ')
        print('Exporting threads to .CSV...')
        df.to_csv(fr'{file_name}', index=False)
        print("Saved! (idk to where tho sorry)")

    elif user_response.lower() == 'n':
        print('ok...')

    else:
        print('Invalid response. Input y/n: ')

#for Reddit comments
elif user_input_command == "/comments":
    print('''
        **ABOUT COMMENTS**
        This script takes a thread URL;
        Analyzes the sentiment of the comments (-1 / 0 / 1);
        Returns a .CSV file of the results.

        documentation: https://praw.readthedocs.io/en/latest/code_overview/models/comment.html
        ''')

    url = input('Input thread URL: ')

    df = get_comments(url)
    sentiment_analysis_comments(df)

    print('----------INFO-----------')

    print("Distribution (sentiment): ")
    display(df.sentiment.value_counts())

    print('-------------------------')

    print("Percent distribution (sentiment): ")
    display(df.sentiment.value_counts(normalize=True) * 100)

    print('-------------------------')

    print("Output sample: ")
    display(df.head())

    user_response = input('Would you like to export as a .CSV file? (y/n): ')

    if user_response.lower() == 'y':
        file_name = input('Input file name: ex) genshin_comments_jv5fdem.csv: ')
        print('Exporting threads to .CSV...')
        df.to_csv(fr'{file_name}', index=False)
        print("Saved! (idk to where tho sorry)")

    elif user_response.lower() == 'n':
        print('ok...')

    else:
        print('Invalid response. Input y/n: ')

#for invalid command inputs
else:
    input('''
    Invalid command. Type a command: 
        
    **COMMANDS**
    /threads - scrapes + analyzes sentiment of headlines in a subreddit. (w/ search words)
    /comments - scrapes + analyzes sentiment of comments in a thread.
    ''')

input('press the ENTER key to end session: ')