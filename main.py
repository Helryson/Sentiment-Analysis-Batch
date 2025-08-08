import os
from dotenv import load_dotenv
import json
import pandas as pd
from sentiment_analysis import Analise_sentimento

if __name__ == "__main__":
    load_dotenv('.env')
    API_KEY = os.getenv('API_KEY')
    PATH_ENTRADA = "Projetos/Datasets/twcs.csv"
    PATH_SAIDA = "./data"
    
    analisador = Analise_sentimento(API_KEY, PATH_ENTRADA)
    print('criou instancia')
    
    tasks = analisador.create_tasks_json(analisador.df)
    print('criou tasks')

    path_tasks = analisador.save_tasks_jsonl(PATH_SAIDA, tasks)
    print('salvou tasks')
    
    sentiment_results = analisador.send_batch_openai(path_tasks)
    print('enviou tasks')
    
    df = analisador.df.copy()
    
    for res in sentiment_results:
        task_id = res['custom_id']
        index = int(task_id.split('-')[-1])
        result = res['response']['body']['choices'][0]['message']['content']
        
        try:
            result_json = json.loads(result)
        except json.JSONDecodeError:
            result_json = {"Sentimento": "", "Explicação": ""}
        
        df.loc[df['index'] == index, 'sentiment_analysis'] = result
        df.loc[df['index'] == index, 'sentiment'] = result_json.get('Sentimento', '')
        df.loc[df['index'] == index, 'sentiment_explanation'] = result_json.get('Explicação', '')
    
    df.to_csv(f"{PATH_SAIDA}/sentiment_analysis_final.csv", index=False)
    
    print("Análise de sentimentos concluída e salva.")
