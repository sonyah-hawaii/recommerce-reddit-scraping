"""
Description: Retrieved subreddit submissions and comments from https://the-eye.eu/redarcs/ and converts to two pickle files
"""

import os

WORKDIR = os.path.dirname(__file__)

import io
import json
import pandas as pd
import zstandard as zstd

####
## [FUNCTION] read_zst_file
####
def read_zst_file(filepath):
    DCTX = zstd.ZstdDecompressor(max_window_size=2147483648)

    with open(filepath, 'rb') as fh:
        stream_reader = DCTX.stream_reader(fh)
        text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')

        data = []
        for line in text_stream:
            data.append(json.loads(line))

    return pd.DataFrame(data)

def get_submissions():
    print('GETTING SUBMISSIONS...')

    folder = os.path.join(WORKDIR, 'input_submissions')
    for file in os.listdir(folder):
        print(f'    > {file}')

        filepath = os.path.join(folder, file)

        df = read_zst_file(filepath)

        df.to_pickle(os.path.join(WORKDIR, 'output_submissions', f'{file.split(".")[0]}.pickle'))

def get_comments():
    print('GETTING COMMENTS...')

    folder = os.path.join(WORKDIR, 'input_comments')
    for file in os.listdir(folder):
        print(f'    > {file}')

        filepath = os.path.join(folder, file)

        df = read_zst_file(filepath)

        df.to_pickle(os.path.join(WORKDIR, 'output_comments', f'{file.split(".")[0]}.pickle'))

def submissions_to_dataframe():
    print('SUBMISSIONS TO DATAFRAME...')

    dfs = []
    folder = os.path.join(WORKDIR, 'output_submissions')
    for file in os.listdir(folder):
        print(f'    > {file}')

        filepath = os.path.join(folder, file)

        df = pd.read_pickle(filepath)
        df.reset_index(drop=True, inplace=True)
        df.insert(0, 'SUBREDDIT', file.split('_')[0])

        dfs.append(df)
    
    dataframe = pd.concat(dfs)
    dataframe.columns = [column.upper() for column in dataframe.columns.tolist()]

    dataframe.to_pickle(os.path.join(WORKDIR, 'submissions.pickle'))

def comments_to_dataframe():
    print('COMMENTS TO DATAFRAME...')

    dfs = []
    folder = os.path.join(WORKDIR, 'output_comments')
    for file in os.listdir(folder):
        print(f'    > {file}')

        filepath = os.path.join(folder, file)

        df = pd.read_pickle(filepath)
        df.reset_index(drop=True, inplace=True)
        df.insert(0, 'SUBREDDIT', file.split('_')[0])

        dfs.append(df)
    
    dataframe = pd.concat(dfs)
    dataframe.columns = [column.upper() for column in dataframe.columns.tolist()]

    dataframe.to_pickle(os.path.join(WORKDIR, 'comments.pickle'))


def main():
    # These will turn the .zst files to .pickle
    # get_submissions()
    # get_comments()

    # Combines all the pickle files into dataframes
    submissions_to_dataframe()
    comments_to_dataframe()


if __name__ == '__main__':
    main()
