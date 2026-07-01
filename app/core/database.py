from app.core.config import settings
from sqlalchemy.orm import Mapped,relationship,DeclarativeBase,sessionmaker
from sqlalchemy import create_engine,ForeignKey,Text,String


class Base(DeclarativeBase):
    pass

database_url=settings.DATABASE_URL


engine=create_engine(database_url,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(bind=engine)

def get_db():
    db=SessionLocal(autoflush=False, autocommit=False)
    try:
        yield db
    finally:
        db.close

