from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker  

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Adjmtw12@board.clgc2eqm2oxu.ap-northeast-2.rds.amazonaws.com:5432/board"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()