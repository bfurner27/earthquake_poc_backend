from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbUrl = environ['DB_URL']

engine = create_engine(dbUrl)
SessionFactory = sessionmaker(bind=engine)
ORMBase = declarative_base()