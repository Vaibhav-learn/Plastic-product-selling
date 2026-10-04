#SQLAlchemy is open source toolkit and Object-Relational Mapper for pyhton programming Language
#Which acts as a bridge between Python applications and relational databases

from sqlalchemy import create_engine
#helps establish connection framework b/w python application and your target database
# in somple is helps open the blue print  to build something

from sqlalchemy.orm import DeclarativeBase, sessionmaker
#DeclarativeBase designs the toys so they fit perfectly inside the chest
#sessionmaker hires the butler who actually carries the toys back and the forth

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL
)
#helps manage database connections

SessionLocal = sessionmaker(
    bind= engine,
    autoflush=False,
    autocommit = False
)
#helps perform database operations
#it create a factory that can produce database

class Base(DeclarativeBase):
    pass

#All SQLAlchemy database models inherits from this class
#represents database tables

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


#FastAPI Database Dependency
#This function
# 1. Creates a database seesion
# 2. Gives that session to the endpoint
# 3. Closes the session after the request finishes
# This prevents database sessions from being left open  