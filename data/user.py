# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from data.base import Base

users_roles_association = Table('UsersRoles', Base.metadata,
    Column('UserId', BigInteger, ForeignKey('Users.UserId')),
    Column('RoleId', BigInteger, ForeignKey('Roles.RoleId'))
)

# movies_actors_association = Table(
#     'movies_actors', Base.metadata,
#     Column('movie_id', Integer, ForeignKey('movies.id')),
#     Column('actor_id', Integer, ForeignKey('actors.id'))
# )



class User(Base):
    __tablename__ = 'Users'

    # id = Column(Integer, primary_key=True)
    # title = Column(String)
    # release_date = Column(Date)
    # actors = relationship("Actor", secondary=movies_actors_association)

    # def __init__(self, title, release_date):
    #     self.title = title
    #     self.release_date = release_date

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