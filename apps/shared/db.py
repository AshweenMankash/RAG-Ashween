from sqlalchemy import create_engine, text
from shared.Models import Base
import os


engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
session.execute(text("CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);"))
session.commit()
session.close()