from transformers import AutoTokenizer, pipeline
import pandas as pd
from .nlp_config import PLACEHOLDER, OUTPUT_FILE, BATCH_SIZE
from typing import List, Dict


def create_pipeline():
    """
    Initializes pipeline for sentiment analysis.

    Change params as needed.
    """
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=model_name,
        tokenizer=tokenizer,
        padding=True,
        truncation=True,
        max_length=512,
        top_k=None
    )
    return sentiment_pipeline


def process_batch(
        batch_texts: List[str],
        pipeline,
        batch_index: int,
        n_batches: int,
        output_file: str = OUTPUT_FILE,
        ) -> List[Dict[str, float]]:
    """
    Function to process one batch of texts.

    Also does some formatting, error handling and outputting.

    Input:
        batch_texts (List[str]): list of texts for analysis
        pipeline: pipeline for analysis
        batch_index: index of batch (for logging)
        n_batches: how many total batches (for logging)
        output_file (str): if provided, writes analysis results here

    Output:
        results (List[Dict[str, float]])
    """
    try:
        print(f"Processing batch {batch_index + 1} / {n_batches}")
        results = pipeline(batch_texts)
        results = [format_scores(r) for r in results]
    except RuntimeError as e:
        print(f"RuntimeError encountered in batch {batch_index + 1}: {e}")
        results = [PLACEHOLDER] * len(batch_texts)
    if output_file:
        df = pd.DataFrame(results)
        df['text'] = batch_texts
        df.to_csv(output_file, mode="a+")
    return results


def format_scores(scores: dict) -> dict:
    return {i['label']: i['score'] for i in scores}


def format_all_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Labels output columns and adds column with highest score label.
    """
    df = df.rename(columns={
        'LABEL_0': 'negative',
        'LABEL_1': 'neutral',
        'LABEL_2': 'positive'
    })

    df['label'] = df.drop(['text', 'label'], axis=1).idxmax(axis=1)
    return df


def make_batches(data, start, batch_size=BATCH_SIZE):
    return [
            data[i:j] for i, j in zip(
                [n for n in range(start, len(data), batch_size)],
                [n for n in range(
                    start+batch_size, len(data)+batch_size, batch_size
                    )],
            )]
