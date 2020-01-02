from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship

from data import base


users_roles_association = Table('Users_Roles', base.Base.metadata,
    Column('UserId', BigInteger, ForeignKey('User.UserId')),
    Column('RoleId', BigInteger, ForeignKey('Role.RoleId'))
)

class User(Base):
    __tablename__ = 'Users'

    UserId = Column(BigInteger, primary_key = True)
    UserIndex = Column(String(8), nullable = False)
    Name = Column(String(32), nullable = False)
    Username = Column(String(32), nullable = False)
    Discriminator = Column(String(4), nullable = False)
    StatusFakultet = Column(String(20))
    StatusDiscord = Column(String(20), nullable = False)
    NumberOfMessages = Column(Integer, default = 0)
    Points = Column(Integer, default = 0)

    Roles = relationship('Role', secondary = users_roles_association)

    def __init__(self, 
        UserId, UserIndex, Name, Username, Discriminator, 
        StatusFakultet, StatusDiscord, NumberOfMessages, Points
    ):
        self.UserId = UserId
        self.UserIndex = UserIndex
        self.Name = Name,
        self.Username = Username
        self.Discriminator = Discriminator
        self.StatusFakultet = StatusFakultet
        self.StatusDiscord = StatusDiscord
        self.NumberOfMessages = NumberOfMessages
        self.Points = Points

