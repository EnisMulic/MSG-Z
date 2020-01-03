# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship, backref

from data.base import Base


class Youtube(Base):
    __tablename__ = 'Youtube'

    ChannelId = Column(String(32), primary_key = True)
    ChannelName = Column(String(256), nullable = False)
    VideoTitle = Column(String(256), nullable = False)
    VideoId = Column(String(32), nullable = False)
    DateTime = Column(DateTime)

    UserId = Column(BigInteger, ForeignKey('Users.UserId'), nullable = True)
    User = relationship('User')

    def __init__(self, ChannelId, ChannelName, VideoTitle, VideoId, User = None):
        self.ChannelId = ChannelId
        self.ChannelName = ChannelName
        self.VideoTitle = VideoTitle
        self.VideoId = VideoId
        self.User = User


    