from cel import app
from shared.embeddings import Embeddings
from shared.Models import *
from shared.db import Session

@app.task(name="tasks.ingestion.ingest_documents")
def ingest_documents(user, document, document_id=None):
    try:
        print(f"[Ingest] User: {user['user_id']} | Doc: {document_id}")
        session = Session()
        
        if document_id:
            session.query(DocumentChunk).filter(DocumentChunk.source_id == document_id).delete()

        metadata = document.get("metadata")
        
        embeddings = Embeddings.generate_embeddings(document['content'], metadata, document.get("title"))
        
        documentMeta = SourceDocument(
            id=embeddings["source_id"],
            title = embeddings["title"],
            doc_metadata = embeddings['doc_metadata']
        )
        session.add(documentMeta)

        for chunk in embeddings['chunks']:
            doc = DocumentChunk(
                id=chunk["id"],
                source_id = documentMeta.id,
                content = chunk['content'],
                chunk_metadata = chunk["chunk_metadata"],
                chunk_index = chunk["chunk_index"],
                embedding = chunk["embedding"],
            )
            session.add(doc)
        session.commit()
        session.close()
        return {"status": "success", "chunk_count": len(embeddings['chunks'])}
    except Exception as e:
        print(f"[Ingest Error] {e}")
        return {"status": "error", "message": str(e)}
