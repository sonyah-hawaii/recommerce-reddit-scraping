import numpy as np
import pandas as pd
import nltk


def other_platform(record) -> bool:
    other_platforms = ['Depop', 'EtsySellers', 'Etsy', 'Flipping', 'Grailed', 'poshmark', 'stockx', 'Mercari', 'ThredUp', 'TheRealReal', 'TRR', 'Ebay']
    platform = posts.loc[record, 'subreddit'].lower()
    other_platforms = [i.lower() for i in other_platforms if i.lower() != platform]
    all_text = str(posts.loc[record,'selftext']) + str(posts.loc[record,'author_flair_text']) + str(posts.loc[record,'poll_data'])
    for n in other_platforms:
        if n in all_text.lower():
            return True
    return False


def poll_options(poll_data: str) -> str:
    if isinstance(poll_data, str):
        poll_data = eval(str(poll_data))
        options = [i['text'] for i in poll_data['options']]
        return ', '.join(options)
   
   
def remove_stopwords(sentence: str) -> str:
    stopwords = nltk.corpus.stopwords.words('english')
    sentence = sentence.split(' ')
    output = [word for word in sentence if word.lower() not in stopwords]
    return ' '.join(output).replace('\n', ' ').strip()
