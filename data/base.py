# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json

with open('.\\config.json') as json_data_file:
    data = json.load(json_data_file)

engine = create_engine(data['Connection-String'])
Session = sessionmaker(bind=engine)

Base = declarative_base()