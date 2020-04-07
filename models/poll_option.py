from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class PollOption(Base):
    __tablename__ = 'PollOptions'

    PollOptionId = Column(Integer, primary_key = True)
    Icon = Column(String, nullable = False)
    Text = Column(String, nullable = False)
    
    PollId = Column(Integer, ForeignKey('Polls.PollId'), nullable = False)
    Poll = relationship('Poll')

    def __init__(self, Icon, Text, Poll):
        self.Icon = Icon
        self.Text = Text
        self.Poll = Poll