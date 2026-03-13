import models
from auth_database import engine, Base

# here i am going to telling sql alchemy to create all the tables that i have mentioned in the models.py file 

Base.metadata.create_all(bind=engine)