from sqlalchemy import Column, String, Integer, DateTime

from models.base import Base

class News(Base):
    __tablename__ = "News"

    Id = Column(Integer, primary_key = True)
    HashedUrl = Column(String, nullable = False, unique = True)
    DateTime = Column(DateTime, nullable = False)


    def __init__(self, id, hashedUrl, dateTime):
        self.Id = id
        self.HashedUrl = hashedUrl
        self.DateTime = dateTime,
