from celery import Celery
from typing import List, Dict
import os


celery_app = Celery(
    "rag_api",
    broker=os.getenv("broker_url"),
    backend=os.getenv("result_backend")
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json'
)

def ingest_documents(user: Dict, documents: List[Dict], document_id: str = None):
    return celery_app.send_task(
        "tasks.ingestion.ingest_documents",
        args=[user, documents, document_id]
    )


def process_query(user: Dict, question: str, filters: Dict = None):
    return celery_app.send_task(
        "tasks.query.process_query",
        args=[user, question, filters]
    )
