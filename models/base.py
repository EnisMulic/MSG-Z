from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

DATABASE_URL = os.environ.get("CONNECTION_STRING")

engine = create_engine(DATABASE_URL, max_overflow = -1)
Session = sessionmaker(bind = engine)

Base = declarative_base()
