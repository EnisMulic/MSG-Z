from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship, backref

from models.base import Base


class Tag(Base):
    __tablename__ = 'Tag'

    Id = Column(Integer, primary_key = True)
    Name = Column(String(256), nullable = False, unique = True)
    Link = Column(String(2084), nullable = False, unique = True)
    Count = Column(Integer, default = 0)
    
    
    UserId = Column(BigInteger, ForeignKey('Users.UserId'), nullable = False)
    User = relationship('User')

    def __init__(self, Name, Link, User, Count = 0):
        self.Name = Name
        self.Link = Link
        self.User = User
        self.Count = Count