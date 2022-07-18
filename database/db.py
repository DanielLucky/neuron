from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BLOB, DateTime, func
from sqlalchemy.orm import declarative_base

DSN = 'postgresql://user:password@db/db'

engine = create_engine(DSN)
Base = declarative_base()




