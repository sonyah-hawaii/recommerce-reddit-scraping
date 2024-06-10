import pandas as pd
from sentiment_analysis_src.nlp_helpers import (
    create_pipeline, process_batch,
    format_all_results, make_batches
    )
from sentiment_analysis_src.nlp_config import OUTPUT_FILE
import multiprocess as mp

if __name__ == '__main__':
    print("*** STARTING SENTIMENT ANALYSIS")
    results = []
    start = 0

    df = pd.read_csv('sentiment_data.csv')
    data = df['selftext'].map(lambda s: s.strip().lower())[start:].to_list()

    batches = make_batches(data, start)
    batches = [(batch, n) for n, batch in enumerate(batches)]
    print(f"*** {len(batches)} TEXT BATCHES TO BE RUN")

    print("*** CREATING PIPELINE ETC")
    sentiment_pipeline = create_pipeline()

    def process_batch_w_pipe(batch):
        batch_index = batch[1]
        batch = batch[0]
        return process_batch(
            batch, sentiment_pipeline, batch_index, len(batches)
        )

    print("*** RUNNING SENTIMENT ANALYSIS")
    with mp.Pool(
        processes=mp.cpu_count(),
    ) as pool:
        results_batches = pool.map(process_batch_w_pipe, batches)

    results_df = format_all_results(pd.read_csv(OUTPUT_FILE))
    results_df.to_csv("FINAL_RESULTS.csv")
    print("*** DONE!")
