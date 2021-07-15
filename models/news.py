from sqlalchemy import Column, String, Integer, DateTime

from models.base import Base

class News(Base):
    __tablename__ = "News"

    Id = Column(Integer, primary_key = True)
    HashedUrl = Column(String, nullable = False, unique = True)
    DateTime = Column(DateTime, nullable = False)
    Source = Column(String(5))


    def __init__(self, hashedUrl, dateTime, source):
        self.HashedUrl = hashedUrl
        self.DateTime = dateTime,
        self.Source = source
