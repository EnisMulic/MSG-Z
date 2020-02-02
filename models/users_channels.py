from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, BigInteger, Float
from sqlalchemy.orm import relationship

from models.base import Base


class UsersChannelsActivity(Base):
    __tablename__ = 'UsersChannelsActivity'

    UserId = Column(BigInteger, ForeignKey('Users.UserId'), primary_key = True)
    ChannelId = Column(BigInteger, ForeignKey('Channels.Id'), primary_key = True)
    NumberOfMessages = Column(Integer, default = 0)
    LengthOfMessages = Column(Integer, default = 0)
    Points = Column(Integer, default = 0)

    User = relationship("User", back_populates = "Channels")
    Channel = relationship("Channel", back_populates = "Users")

    def __init__(self, UserId, ChannelId, NumberOfMessages = 0, LengthOfMessages = 0, Points = 0):
        self.UserId = UserId
        self.ChannelId = ChannelId
        self.NumberOfMessages = NumberOfMessages
        self.LengthOfMessages = LengthOfMessages
        self.Points = Points

