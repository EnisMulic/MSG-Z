from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship, backref

from models.base import Base

class Tag(Base):
    __tablename__ = 'Tags'

    Id = Column(Integer, primary_key = True)
    Name = Column(String(100), nullable = False, unique = True)
    Content = Column(String(2000), nullable = False, unique = True)
    Type = Column(String(20)) # LinkTag or TextTag
    Count = Column(Integer, default = 0)
    Created = Column(DateTime)
    
    
    UserId = Column(BigInteger, ForeignKey('Users.UserId'), nullable = True)
    User = relationship('User')

    def __init__(self, Name, Link, Created, User, Count = 0):
        self.Name = Name
        self.Link = Link
        self.Created = Created
        self.User = User
        self.Count = Count