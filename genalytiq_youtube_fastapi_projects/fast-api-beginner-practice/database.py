from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

MYSQL_USER  = "root"
MYSQL_PASSWORD  =urllib.parse.quote_plus("2394Venu@")
MYSQL_HOST  = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "fastapi_genlytiq_db"

# 1. The Connection String
# Format : mysql+driver://user:password@host:port/database_name
# Make sure to replace "'YOUR_PASSWORD_HERE' with your actual root password"
# py msql is a connector. It helps python to talk with myql 
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


# 2. The Engine 
# This is the core interface to the database. It manages the connection pool.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. The Session
# Each time a request comes in, we create a temporary "session" to talk to the DB, then close it.
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)


def get_db():
    """Get a database session. This is a generator function."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. The Base
# Declarative base is basically where all the SQL alchemy models will be inheritted from.
Base = declarative_base()