from sqlalchemy import Column, Integer, String, BigInteger, Table, ForeignKey

from data import base


# users_roles_association = Table('Users_Roles', base.Base.metadata,
#     Column('UserId', BigInteger, ForeignKey('User.UserId')),
#     Column('RoleId', BigInteger, ForeignKey('Role.RoleId'))
# )

class Role(Base):
    __tablename__ = 'Roles'

    RoleId = Column(BigInteger, primary_key = True)
    Name = Column(String(32), nullable = False)

    # Users = db.relationship('User', secondary = users_roles_association)

    def __init__(self, RoleId, Name):
        self.RoleId = RoleId
        self.Name = Name
        