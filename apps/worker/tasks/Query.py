from main import app
from shared.embeddings import Embeddings
from shared.llm import generate_answer

@app.task(name="tasks.query.process_query")
def process_query(user, question, filters=None):
    try:
        print(f"[Query] User: {user['user_id']} | Q: {question[:50]}")

        question_embedding = Embeddings.generate_embeddings(question)
        
        # context_docs = retrieve_top_k(user_id=user["user_id"], embedding=question_embedding, filters=filters, k=5)

        context = "\n".join([doc["content"] for doc in context_docs])

        answer = generate_answer(question, context)

        return {
            "status": "success",
            "answer": answer,
            "context_used": [doc["id"] for doc in context_docs]
        }
    except Exception as e:
        print(f"[Query Error] {e}")
        return {"status": "error", "message": str(e)}
