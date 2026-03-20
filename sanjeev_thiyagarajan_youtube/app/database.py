from time import time

import psycopg2
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib.parse
import psycopg2
from app.config import settings


MYSQL_PASSWORD  =urllib.parse.quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URI = f"postgresql://{settings.database_username}:{MYSQL_PASSWORD}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URI)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#  just for refrence purpose we are not using this
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="2394Venu@",
#             cursor_factory=RealDictCursor
#             )
#         cursor = conn.cursor()
#         print('data base connected')
#         break
        
#     except Exception as err:
#         print('Error connecting to database:', err)
#         time.sleep(2)