from transformers import AutoTokenizer, pipeline
import pandas as pd
from .nlp_config import (
    PLACEHOLDER, INPUT_FILE, OUTPUT_FILE, BATCH_SIZE, 
    MODEL_PATH, TEXT_COL, ID_COL)
from typing import List, Dict, Callable, Any


def text_preprocessor(text: str):
    return text.strip().lower()


def import_and_preprocess_text(
        input_file: str = INPUT_FILE,
        preprocessor_func: Callable = text_preprocessor
        ) -> pd.DataFrame:
    df = pd.read_csv(input_file)[[ID_COL, TEXT_COL]]
    df['processed_text'] = df[TEXT_COL].map(preprocessor_func)
    df.drop(TEXT_COL, axis=1, inplace=True)
    return df


def create_pipeline():
    """
    Initializes pipeline for sentiment analysis.

    Change params as needed.
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=MODEL_PATH,
        tokenizer=tokenizer,
        padding=True,
        truncation=True,
        max_length=512,
        top_k=None
    )
    return sentiment_pipeline


def process_batch(
        batch_data: List[List[str]],
        pipeline,
        batch_index: int,
        n_batches: int,
        output_file: str = OUTPUT_FILE,
        ) -> List[Dict[str, Any]]:
    """
    Function to process one batch of texts.

    Also does some formatting, error handling and outputting.

    Input:
        batch_data(List[List[str, str]]): list of (id, text) for analysis
        pipeline: pipeline for analysis
        batch_index: index of batch (for logging)
        n_batches: how many total batches (for logging)
        output_file (str): if provided, writes analysis results here

    Output:
        results (List[Dict[str, Any]])
    """
    try:
        print(f"Processing batch {batch_index + 1} / {n_batches}")
        text_ids, batch_texts = map(list, zip(*batch_data))
        results = pipeline(batch_texts)
        results = [
            format_scores(r, id=id_)
            for r, id_ in zip(results, text_ids)
            ]
    except RuntimeError as e:
        print(f"RuntimeError encountered in batch {batch_index + 1}: {e}")
        results = [PLACEHOLDER] * len(batch_texts)
    if output_file:
        df = pd.DataFrame(results)
        df['text'] = batch_texts
        df.to_csv(output_file, mode="a+")
    return results


def format_scores(scores: dict, **kwargs) -> dict:
    output = {i['label']: i['score'] for i in scores}
    output.update(kwargs)
    return output


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


def make_batches(data, start=0, batch_size=BATCH_SIZE,
                 add_indexes: bool = True):
    batches = [
            data[i:j] for i, j in zip(
                [n for n in range(start, len(data), batch_size)],
                [n for n in range(
                    start+batch_size, len(data)+batch_size, batch_size
                    )],
            )]
    if add_indexes:
        batches = [(batch, n) for n, batch in enumerate(batches)]
    return batches
