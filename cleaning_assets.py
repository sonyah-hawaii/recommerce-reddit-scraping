# initial file dicts
all_comments = {}
all_posts = {}
# cleaned file dicts
posts_cleaned = {}
comments_cleaned = {}
# metadata containers
comments_full = []
comments_unique = []
comments_pct_removed = []
unique_linked_posts = []
posts_full = []
posts_unique = []
posts_pct_removed = []
start_dates = []
end_dates = []
# relevant columns from comments
comments_cols = [
    # subreddit
    'subreddit_id', 'subreddit', 'subreddit_type',
    # record identity
    'id', 'parent_id', 'link_id', 'author', 'created_utc',
    # interactions
    'score', 'controversiality', 'ups', 'likes',
    # contents
    'body', 'author_flair_text'
    ]
# relevant columns from posts
posts_cols = [
    # subreddit
    'subreddit', 'subreddit_id', 'subreddit_type',
    # record identity
    'id', 'name', 'media', 'is_video', 'created_utc',
    # interactions
    'num_comments', 'score', 'ups',
    # contents
    'selftext', 'author_flair_text', 'link_flair_text', 'poll_data'
]
# datatypes for comments
comments_datatypes = {
    'subreddit_id': str,
    'subreddit': str,
    'subreddit_type': str,
    'id': str,
    'parent_id': str,
    'link_id': str,
    'author': str,
    'created_utc': int,
    'score': int,
    'controversiality': bool,
    'ups': int,
    'likes': int,
    'body': str,
    'author_flair_text': str
}
# datatypes for posts
posts_datatypes = {
    'subreddit': str,
    'subreddit_id': str,
    'subreddit_type': str,
    'id': str,
    'name': str,
    'media': str,
    'is_video': bool,
    'created_utc': int,
    'num_comments': int,
    'score': int,
    'ups': int,
    'selftext': str,
    'author_flair_text': str,
    'link_flair_text': str,
    'poll_data': str
}

comments_cols_convert = {key: value for key, value
                         in comments_datatypes.items() if value != str}
posts_cols_convert = {key: value for key, value
                      in posts_datatypes.items() if value != str}
