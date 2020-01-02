from sqlalchemy import relationship
from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey

from data import base

class Post(Base):
    __tablenames__ = 'Posts'

    PostId = Column(BigInteger, primary_key = True)
    ChannelId = Column(BigInteger, nullable = False)
    UserId = Column(BigInteger, ForeignKey('User.UserId'))
    User = relationship('User')

    def __init__(self, PostId, ChannelId, UserId = null):
        self.PostId = PostId
        self.ChannelId = ChannelId
        self.UserId = UserId