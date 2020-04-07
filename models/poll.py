from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class Poll(Base):
    __tablename__ = 'Polls'

    PollId = Column(Integer, primary_key = True)
    MessageId = Column(BigInteger, nullable = True)
    ChannelId = Column(BigInteger, nullable = True)
    Name = Column(String, nullable = False, unique = True)

    UserId = Column(BigInteger, ForeignKey('Users.UserId'))
    User = relationship('User')

    def __init__(self, Name, MessageId = None, ChannelId = None, UserId = None):
        self.Name = Name
        self.MessageId = MessageId
        self.ChannelId = ChannelId
        self.UserId = UserId