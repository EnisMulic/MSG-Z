from sqlalchemy import Column, String, BigInteger

from models.base import Base


class User(Base):
    __tablename__ = "Users"

    DiscordId = Column(BigInteger, primary_key = True)
    Index = Column(String(8), nullable = False, unique = True)
    Name = Column(String(32), nullable = False)
    Username = Column(String(32), nullable = False)
    Discriminator = Column(String(4), nullable = False)

    def __init__(self, discordId, index, name, username, discriminator):
        self.DiscordId = discordId
        self.Index = index
        self.Name = name,
        self.Username = username
        self.Discriminator = discriminator
