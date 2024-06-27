OUTPUT_FILE = 'output_clean.csv'
INPUT_FILE = 'sentiment_data.csv'
TEXT_COL = "selftext"
ID_COL = 'id'

MODEL_PATH = "cardiffnlp/twitter-roberta-base-sentiment"

BATCH_SIZE = 256
PLACEHOLDER = {'label': 'na', 'score': 0}
