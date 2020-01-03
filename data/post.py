from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship

from data.base import Base

class Post(Base):
    __tablename__ = 'Posts'

    PostId = Column(BigInteger, primary_key = True)
    ChannelId = Column(BigInteger, nullable = False)
    UserId = Column(BigInteger, ForeignKey('Users.UserId'))
    User = relationship('User')

    def __init__(self, PostId, ChannelId, User = None):
        self.PostId = PostId
        self.ChannelId = ChannelId
        self.User = User