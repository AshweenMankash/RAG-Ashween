from shared.db import Session
from shared.Models import DocumentChunk
from shared.embeddings import Embeddings

def search_similar_chunks(query: str, top_k: int = 2, doc_id=None):
    
    embedding_result = Embeddings.generate_embedding_without_chunking(query)
    query_embedding = embedding_result  # only 1 chunk
    session = Session()

    

    results = (
        session.query(DocumentChunk)
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))  # or .cosine_distance(query_embedding)
        .limit(top_k)
        .all()
    )
    session.close()
    return results