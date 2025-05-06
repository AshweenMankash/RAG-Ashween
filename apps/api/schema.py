from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict

class UserMetadata(BaseModel):
    user_id: str
    session_id: Optional[str] = None

class DocumentIn(BaseModel):
    content: Optional[str]
    metadata: Optional[Dict] = {}
    title: Optional[str] = None

class IngestRequest(BaseModel):
    user: UserMetadata
    document: DocumentIn

class QueryRequest(BaseModel):
    user: UserMetadata
    question: str
    filters: Optional[Dict] = None
    document_id: Optional[str] = None


class TaskResponse(BaseModel):
    task_id: str

class ResultResponse(BaseModel):
    status: str
    result: Optional[str] = None
    error: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"