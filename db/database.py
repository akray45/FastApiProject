from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQL_DATABASE = "sqlite:///.dummy.db"
"""SQlite and sqlalchemy setup"""
engine = create_engine(SQL_DATABASE, echo=True)
SESSION = sessionmaker(bind= engine)

Base = declarative_base()
