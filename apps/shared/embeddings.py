import uuid
from typing import Dict, List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# Initialize once
model = SentenceTransformer('/app/Model/all-MiniLM-L6-v2/')
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=50
)   
class Embeddings:
    @staticmethod
    def generate_embeddings(text: str, metadata: Dict = None, title: str = "") -> Dict:
        """
        Split text and generate OpenAI embeddings using LangChain.
        Returns a dict with source_id and list of chunks (with embeddings).
        """
        chunks = splitter.split_text(text)
        embeddings = model.encode(chunks)

        source_id = str(uuid.uuid4())
        data = []

        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            data.append({
                "id": str(uuid.uuid4()),
                "source_id": source_id,
                "chunk_index": idx,
                "content": chunk,
                "embedding": vector,
                "chunk_metadata": metadata or {}
            })

        return {
            "source_id": source_id,
            "title": title,
            "doc_metadata": metadata or {},
            "chunks": data
        }

    @staticmethod
    def generate_embedding_without_chunking(text):
        """
        Generate embeddings without chunking.
        Returns a dict with source_id and list of chunks (with embeddings).
        """
        vector = model.encode(text)
        
        return vector