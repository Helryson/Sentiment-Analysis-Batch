import json
import os
import pandas as pd
from pathlib import Path
from sentiment_analysis import Analise_sentimento

def test_create_tasks_json(monkeypatch):
    df = pd.DataFrame({
        'index': [0, 1],
        'chat_conversation': ['Mensagem positiva', 'Mensagem negativa']
    })

    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: df)

    analise = Analise_sentimento(API_KEY='Qualquer key', path='Qualquer path')

    tasks = analise.create_tasks_json(df)

    assert len(tasks) == 2

    for task in tasks:
        assert "custom_id" in task
        assert "method" in task
        assert "url" in task
        assert "body" in task

def test_save_tasks_jsonl(monkeypatch, tmp_path):
    df = pd.DataFrame({
        'index': [0, 1],
        'chat_conversation': ['Mensagem positiva', 'Mensagem negativa']
    })

    tasks = [
        {"custom_id": "task-0", "method": "POST", "url": "/v1/chat/completions", "body": {"test": 1}},
        {"custom_id": "task-1", "method": "POST", "url": "/v1/chat/completions", "body": {"test": 2}}
    ]

    monkeypatch.setattr(pd, "read_csv", lambda *args, **kwargs: df)

    analise = Analise_sentimento(API_KEY='Qualquer key', path=str(tmp_path))

    output_file_path = analise.save_tasks_jsonl(str(tmp_path), tasks)

    assert os.path.isfile(output_file_path)

    with open(output_file_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == len(tasks)

    for line, task in zip(lines, tasks):
        loaded = json.loads(line)
        assert loaded == task

    assert Path(output_file_path) == Path(tmp_path) / 'batch_sentiment_tasks.jsonl'