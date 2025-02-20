from sqlalchemy import Engine, create_engine, select, Table, Column, Integer, ForeignKey, String, DATETIME
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()



engine: Engine = create_engine('sqlite:///example.db')
Session: sessionmaker = sessionmaker(bind=engine)
session = Session()


