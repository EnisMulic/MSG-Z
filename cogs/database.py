import discord
from discord.ext import commands

import MySQLdb
import json


def getPassword():
    with open('.\\config.json') as json_data_file:
        data = json.load(json_data_file)
    return data["Database"]["Password"]


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.db = MySQLdb.connect(\
            host = "localhost", \
            user = "root", \
            passwd = getPassword(), \
            db = "FIT_Community", \
            charset = 'UTF8' \
        )

        self.cursor = self.db.cursor()
        self.setup_database_tables()
     
    def setup_database_tables(self):
        try:
            tableUsersQuery = "CREATE TABLE IF NOT EXISTS Users\
                (\
                    UserID BIGINT NOT NULL PRIMARY KEY,\
                    UserIndex NVARCHAR(8) NOT NULL, \
                    Name NVARCHAR(32) NOT NULL,\
                    Username NVARCHAR(32) NOT NULL,\
                    Discriminator VARCHAR(4) NOT NULL,\
                    StatusFakultet NVARCHAR(20),\
                    StatusDiscord NVARCHAR(20) NOT NULL,\
                    NumberOfPosts INT DEFAULT 0 \
                )"
            self.cursor.execute(tableUsersQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Users: Something went wrong: " + str(err))
            pass

        try:
            tableRolesQuery = "CREATE TABLE IF NOT EXISTS Roles\
                (\
                    RoleID BIGINT NOT NULL PRIMARY KEY, \
                    RoleName NVARCHAR(32) NOT NULL \
                )"
            self.cursor.execute(tableRolesQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Roles: Something went wrong: " + str(err))
            pass

        try:
            tableUsersRolesQuery = "CREATE TABLE IF NOT EXISTS UsersRoles\
                (\
                    UserID BIGINT NOT NULL, \
                    RoleID BIGINT NOT NULL, \
                    FOREIGN KEY (UserID) REFERENCES Users(UserID), \
                    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID), \
                    PRIMARY KEY (UserID, RoleID) \
                )"
            self.cursor.execute(tableUsersRolesQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table UsersRoles: Something went wrong: " + str(err))
            pass

        try:
            tablePostsQuery = "CREATE TABLE IF NOT EXISTS Posts\
                (\
                    PostID BIGINT NOT NULL PRIMARY KEY, \
                    ChannelID BIGINT NOT NULL, \
                    UserID BIGINT NOT NULL, \
                    FOREIGN KEY (UserID) REFERENCES Users(UserID) \
                )"
            self.cursor.execute(tablePostsQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Posts: Something went wrong: " + str(err))
            pass
    
    @commands.command(aliases=["insert-role"])
    @commands.has_any_role('Administrator')   
    async def insert_role(self, ctx, role: discord.Role):
        try:
            InsertRoleQuery = 'INSERT INTO Roles(RoleID, RoleName) \
                               VALUES({}, "{}");'.format(
                                   role.id, 
                                   role.name
                                )
            self.cursor.execute(InsertRoleQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Insert Role: Something went wrong: " + str(err))
            pass
        pass

    async def insert_member(self, ctx, member: discord.Member, UserIndex):
        try:
            insertMemberQuery = 'INSERT INTO Users(\
                                    UserID, \
                                    UserIndex, \
                                    Name,\
                                    Username, \
                                    Discriminator, \
                                    StatusFakultet, \
                                    StatusDiscord\
                                )\
                                VALUES(\
                                     {},\
                                    "{}",\
                                    "{}",\
                                    "{}",\
                                    "{}",\
                                    "{}",\
                                    "{}"\
                                );'.format(
                                    member.id,
                                    UserIndex, 
                                    member.nick, 
                                    member.name, 
                                    member.discriminator,
                                    "Aktivan", 
                                    "Aktivan"
                                )

            self.cursor.execute(insertMemberQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Insert Member: Something went wrong: " + str(err))
            pass
        pass

    async def change_member_index(self, ctx, member: discord.Member, UserIndex):
        try:
            changeMemberUserIndexQuery = 'UPDATE Users\
                                          SET UserIndex = "{}"\
                                          WHERE UserID = {};'.format(
                                                UserIndex,
                                                member.id
                                            )
            
            self.cursor.execute(changeMemberUserIndexQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member UserIndex: Something went wrong: " + str(err))
            pass
        pass    

    async def change_member_fakultet_status(self, ctx, member: discord.Member, status):
        try:
            changeMemberFakultetStatusQuery = 'UPDATE Users\
                                               SET StatusFakultet = "{}"\
                                               WHERE UserID = {};'.format(
                                                   status,
                                                   member.id
                                               )
            
            self.cursor.execute(changeMemberFakultetStatusQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Fakultet Status: Something went wrong: " + str(err))
            pass
        pass

    async def change_member_discord_status(self, ctx, member: discord.Member, status):
        try:
            changeMemberDiscordStatusQuery = 'UPDATE Users\
                                              SET StatusDiscord = "{}"\
                                              WHERE UserID = {};'.format(
                                                  status,
                                                  member.id
                                                )
            
            self.cursor.execute(changeMemberDiscordStatusQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Discord Status: Something went wrong: " + str(err))
            pass
        pass

        # Change users in-server nickname
    async def change_member_name(self, ctx, member: discord.Member, name):
        try:
            changeMemberNameQuery = 'UPDATE Users\
                                     SET Name = "{}"\
                                     WHERE UserID = {}'.format(
                                                name, 
                                                member.id
                                            ) 
            
            self.cursor.execute(changeMemberNameQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Name: Something went wrong: " + str(err))
            pass
        pass

    async def change_member_username(self, member: discord.Member):
        try:
            changeMemberUsernameQuery = 'UPDATE Users\
                                         SET Username = "{}"\
                                         WHERE UserID = {};'.format(
                                                   member.name,
                                                   member.id
                                               )
            
            self.cursor.execute(changeMemberUsernameQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Username: Something went wrong: " + str(err))
            pass
        pass

    #probably works?
    async def change_member_discriminator(self, member: discord.Member):
        try:
            changeMemberDiscriminatorQuery = 'UPDATE Users\
                                              SET Discriminator = "{}"\
                                              WHERE UserID = {};'.format(
                                                        member.discriminator,
                                                        member.id
                                                    )
            
            self.cursor.execute(changeMemberDiscriminatorQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Disciminator: Something went wrong: " + str(err))
            pass
        pass

    async def insert_users_role(self, member: discord.Member, role: discord.Role):
        try:
            insertUsersRoleQuery = 'INSERT INTO UsersRoles(RoleID, UserID)\
                                    VALUES({}, {});'.format(
                                        role.id,
                                        member.id
                                    )
            
            self.cursor.execute(insertUsersRoleQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Insert Users Role: Something went wrong: " + str(err))
            pass
        pass

    async def insert_post(self, ctx, channelID, messageID):
        try:
            InsertPostQuery = 'INSERT INTO Posts(PostID, ChannelID, UserID) \
                               VALUES({}, {}, {});'.format(
                                   messageID, 
                                   channelID, 
                                   ctx.author.id
                                )

            self.cursor.execute(InsertPostQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Insert Post: Somethin went wrong: " + str(err))
            pass
        pass

    

    

def setup(client):
    client.add_cog(Database(client))

