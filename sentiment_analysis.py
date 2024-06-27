import pandas as pd
from sentiment_analysis_src.nlp_helpers import (
    create_pipeline, process_batch,
    format_all_results, make_batches,
    import_and_preprocess_text
    )
from sentiment_analysis_src.nlp_config import OUTPUT_FILE
import multiprocess as mp

if __name__ == '__main__':
    print("*** STARTING SENTIMENT ANALYSIS")
    results = []
    start = 0

    prepped_df = import_and_preprocess_text()

    # make_batches adds a batch index by default
    batches = make_batches(prepped_df.values, start)
    print(f"*** {len(batches)} TEXT BATCHES TO BE RUN")

    print("*** CREATING PIPELINE ETC")
    sentiment_pipeline = create_pipeline()

    def process_batch_w_pipe(batch):
        """
        functools.partial isn't compatible with starmap for reasons...
        so we have to make the partial function manually

        formatting is not the cleanest!

        Input:
            batch: [[id, text], batch_index]
        Output:
            process_batch with batch, pipeline, batch_index and n_batches

        """
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
