# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from models.base import Base

users_roles_association = Table('UsersRoles', Base.metadata,
    Column('UserId', BigInteger, ForeignKey('Users.UserId')),
    Column('RoleId', BigInteger, ForeignKey('Roles.RoleId'))
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
        StatusFakultet, StatusDiscord, NumberOfMessages, Points, Roles = None
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
        self.Roles = Roles