from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
import uuid

Base = declarative_base()

class SourceDocument(Base):
    __tablename__ = 'source_documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    doc_metadata = Column(JSON, nullable=True)
    user_id = Column(String, nullable=True)
    chunks = relationship("DocumentChunk", back_populates="source")

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey('source_documents.id'), nullable=False)
    chunk_index = Column(Integer, nullable=False)                  
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=False)
    chunk_metadata = Column(JSON, nullable=True)
    source = relationship("SourceDocument", back_populates="chunks")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

