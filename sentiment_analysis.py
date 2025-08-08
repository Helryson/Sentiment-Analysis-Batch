from config.conteudo_input import CONTEUDO_INPUT
from config.sistema_input import SISTEMA_INPUT
import json
from openai import OpenAI
import os
import pandas as pd
import utils

class Analise_sentimento:

    def __init__(self, API_KEY, path):
        self.client = OpenAI(api_key=API_KEY)
        self.path = path
        self.df = self.load_data()

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.path)
        df.rename(columns={'text': 'chat_conversation'}, inplace=True)
        df = df.reset_index()
        df = df[:1000]
        return df
    
    def create_tasks_json(self, df: pd.DataFrame) -> list:
        sentiment_tasks = []
        for _, row in df.iterrows():
            chat = row["chat_conversation"]
            index = row["index"]
            description_sentiment = CONTEUDO_INPUT.format(linha_conversa=chat)
            sentiment_task = {
                "custom_id": f"task-{index}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-mini",
                    "temperature": 0.1,
                    "response_format": { 
                        "type": "json_object"
                    },
                    "messages": [
                        {
                            "role": "system",
                            "content": SISTEMA_INPUT
                        },
                        {
                            "role": "user",
                            "content": description_sentiment
                        }
                    ],
                }
            }
            sentiment_tasks.append(sentiment_task)

        return sentiment_tasks
    
    def save_tasks_jsonl(self, path: str, sentiment_task_list: list) -> str:
        self.path = path
        sentiment_file = f'{path}/batch_sentiment_tasks.jsonl'
        with open(sentiment_file, 'w') as file:
            for obj in sentiment_task_list:
                file.write(json.dumps(obj) + '\n')
        
        return sentiment_file

    def send_batch_openai(self, sentiment_file: str) -> list:
        sentiment_batch_file = self.client.files.create(
            file=open(sentiment_file, "rb"),
            purpose="batch"
        )
        sentiment_batch_job = self.client.batches.create(
            input_file_id=sentiment_batch_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h"
        )
    
        result = utils.await_result_batch(client=self.client, sentiment_batch_job=sentiment_batch_job)

        result_file_name = f"{self.path}/sentiment_batch_job_results.jsonl"
        with open(result_file_name, 'wb') as file:
            file.write(result)

        return utils.load_results(result_file_name=result_file_name)