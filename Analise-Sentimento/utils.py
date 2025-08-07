import time
import json

import time
import sys

def await_result_batch(client, sentiment_batch_job) -> bytes:
    while True:
        batch_job = client.batches.retrieve(sentiment_batch_job.id)
        if batch_job.status == 'completed':
            break
        elif batch_job.status == 'failed':
            raise Exception("Batch job failed.")
        time.sleep(10)

    result_file_id = batch_job.output_file_id
    result = client.files.content(result_file_id).content

    return result

def load_results(result_file_name):
    sentiment_results = []
    with open(result_file_name, 'r') as file:
        for line in file:
            json_object = json.loads(line.strip())
            sentiment_results.append(json_object)

    return sentiment_results