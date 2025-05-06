from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from schema import *
from celery.result import AsyncResult
from tasks import ingest_documents, process_query
from shared.db import Session
from shared.Models import DocumentChunk, SourceDocument, User
from security import *
from datetime import datetime
import json
from shared.vector_store import search_similar_chunks
import os
import tempfile
import io
from PyPDF2 import PdfReader

# from shared.vector_store import 

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}





@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    
    db = Session()

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}





@app.post("/signin", response_model=TokenResponse)
def signin(user: UserLogin):
    db = Session()
    
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": db_user.email})
    
    return TokenResponse(access_token=token)





@app.post("/ingest", response_model=TaskResponse)
async def ingest_docs(file: UploadFile=None, user: User = Depends(get_current_user)):

    if file is not None:
        file_extension = file.filename.split(".")[-1]
        
        if file_extension not in ["pdf", "txt"]:
            raise Exception("File extension not supported")
        
        
        file_data = await file.read()
        if file.filename.endswith(".txt"):
            text = file_data.decode("utf-8", errors="ignore")
        
        elif file.filename.endswith(".pdf"):
            pdf_file = io.BytesIO(file_data)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

        doc = {"document": {"content": text, "title": file.filename, "metadata": {}},'user': {'user_id': user.id}}
    else:
        raise Exception("No File Given")
    
    
    ingest_documents(user=doc['user'], documents=doc['document'])
    
    return {
        "msg": "Your document has been processed"
    }

@app.post("/query")
def ask_question(req: QueryRequest, user: User = Depends(get_current_user)):
    
    result  = search_similar_chunks(req.question, 5)
    API_KEY  = os.getenv("OPEN_ROUTER_API_KEY")
    import requests

    PROMPT = f"""
        Based on the given context 
        {"   ".join([d.content for d in result])}
        Answer this question:
        {req.question}


        Do not make up answers from any other source other than the context provided.
        If the answer is not in the context, say "I don't know".
        Answer in a concise manner.
        correct grammar and spelling.
        """

    payload = { 
        "model": "openai/gpt-3.5-turbo",
        "prompt":  PROMPT
        }


    resp = requests.post("https://openrouter.ai/api/v1/completions", headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}, json=payload)

    return {
        "answer": resp.json()["choices"][0]["text"],
        "context": [d.content for d in result],
    }

    

@app.get("/documents/{user_id}")
def get_documents(user_id: str):
    session = Session()
    documents = session.query(SourceDocument).all()
    session.close()
    return {
        "data": [d.__dict__ for d in  documents]
    }