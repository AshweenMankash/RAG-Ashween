from celery import Celery
import os
from shared.db import Session

app = Celery(
    "rag_worker",
    broker=os.getenv("broker_url"),
    backend=os.getenv("result_backend")
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json'
)

# app.autodiscover_tasks(["tasks"])
