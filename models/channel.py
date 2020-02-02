from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from models.base import Base


class Channel(Base):
    __tablename__ = 'Channels'

    Id = Column(BigInteger, primary_key = True)
    Name = Column(String(32), nullable = False)
    
    Users = relationship('UsersChannelsActivity', back_populates = "Channel")

    def __init__(self, Id, Name):
        self.Id = Id
        self.Name = Name