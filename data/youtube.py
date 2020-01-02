from sqlalchemy import relationship
from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey

from data import base

class Youtube(Base):
    __tablenames__ = 'Youtube'

    ChannelId = Column(String(32), primary_key = True)
    ChannelName = Column(String(256), nullable = False)
    VideoTitle = Column(String(256), nullable = False)
    VideoId = Column(String(32), nullable = False)

    UserId = Column(BigInteger, ForeignKey('User.UserId'), nullable = True)
    User = relationship('User')

    def __init__(self, ChannelId, ChannelName, VideoTitle, VideoId, UserId = null):
        self.ChannelId = ChannelId
        self.ChannelName = ChannelName
        self.VideoTitle = VideoTitle
        self.VideoId = VideoId
        self.UserId = UserId


    