import discord
from discord.ext import commands
from discord.ext import tasks

import MySQLdb
import json

from utils import misc

def getDatabaseParamater(param):
    with open('.\\config.json') as json_data_file:
        data = json.load(json_data_file)
    return data["Database"][param]


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.db = MySQLdb.connect(\
            host = getDatabaseParamater("host"), \
            user = getDatabaseParamater("user"), \
            passwd = getDatabaseParamater("password"), \
            db = getDatabaseParamater("database_name"), \
            charset = 'UTF8' \
        )

        self.cursor = self.db.cursor()
        self.setup_database_tables()
        self.detect_anomalies.start()

    
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
                    StatusDiscord NVARCHAR(20) NOT NULL\
                )"
            self.cursor.execute(tableUsersQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Users: Something went wrong: " + str(err))
            

        try:
            tableRolesQuery = "CREATE TABLE IF NOT EXISTS Roles\
                (\
                    RoleID BIGINT NOT NULL PRIMARY KEY, \
                    RoleName NVARCHAR(32) NOT NULL \
                )"
            self.cursor.execute(tableRolesQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Roles: Something went wrong: " + str(err))
            

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
            

    @commands.command(aliases=["insert-role"], description = "Add role to the database")
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
                

    async def change_member_fakultet_status(self, member: discord.Member, status):
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
            

    async def change_member_discord_status(self, member: discord.Member, status):
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
            

        # Change users in-server nickname
    async def change_member_name(self, member: discord.Member, name):
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

    async def remove_users_role(self, member: discord.Member, role: discord.Role):
        try:
            removeUsersRoleQuery = 'DELETE FROM USERSROLES\
                                    WHERE RoleID = {} AND UserID = {};'.format(
                                        role.id,
                                        member.id
                                    )
            
            self.cursor.execute(removeUsersRoleQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Remove Users Role: Something went wrong: " + str(err))
            

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
            

    @commands.command(aliases=["get-member-userID", "get-member-uid"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def get_member_by_UserID(self, ctx, member: discord.Member):
        try:
            getMemberQuery = 'SELECT * FROM Users WHERE UserID = {};'.format(member.id)
            self.cursor.execute(getMemberQuery)
            self.db.commit()
            records = self.cursor.fetchall()

            
            for record in records:
                await ctx.send('```\nIme i prezime: {}\nIndex: {}\nUsername: {}\nFakultet: {}\nDiscord: {}\n```'.format(
                            record[2],
                            record[1],
                            record[3] + "#" + record[4],
                            record[5],
                            record[6]
                        ))

        except MySQLdb.ProgrammingError as err:
            print("Procedure Get Member (by UserID): Smething went wrong: " + str(err))
            

    @commands.command(aliases=["get-member-index", "get-member-idx"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def get_member_by_UserIndex(self, ctx, userIndex: str):
        try:
            getMemberQuery = 'SELECT * FROM Users WHERE UserIndex = "{}";'.format(userIndex)
            self.cursor.execute(getMemberQuery)
            self.db.commit()
            records = self.cursor.fetchall()
            
            for record in records:
                await ctx.send('```\nIme i prezime: {}\nIndex: {}\nUsername: {}\nFakultet: {}\nDiscord: {}\n```'.format(
                            record[2],
                            record[1],
                            record[3] + "#" + record[4],
                            record[5],
                            record[6]
                        ))

        except MySQLdb.ProgrammingError as err:
            print("Procedure Get Member (by UserIndex): Smething went wrong: " + str(err))
        

    async def remove_member(self, member: discord.Member):
        try:
            clearMemberQuery = 'DELETE FROM USERSROLES WHERE UserID = {};'.format(member.id)
            self.cursor.execute(clearMemberQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Clear Member: Something went wrong: " + str(err))
        

    @tasks.loop(hours = 7 * 24)
    async def detect_anomalies(self):
        print("Anomalysing...")

        self.cursor.execute('SELECT RoleID FROM ROLES')
        allRolesInDB = self.cursor.fetchall()
        allRoles = []
        for role in allRolesInDB:
            allRoles.append(role[0])

        for guild in self.client.guilds:                                                        
            for member in guild.members:
                try:
                    self.cursor.execute(
                        'SELECT Name, Username, Discriminator FROM USERS WHERE UserID = {};'.format(member.id)
                    )
                

                    memberInDB = self.cursor.fetchone()
                    if memberInDB is not None:
                        if memberInDB[0] != member.nick:
                            await self.change_member_name(member, member.nick)
                                
                        if memberInDB[1] != member.name:
                            await self.change_member_username(member)
                            
                        if memberInDB[2] != member.discriminator:
                            await self.change_member_discriminator(member)

                        self.cursor.execute('SELECT UR.RoleID\
                                            FROM USERS AS U INNER JOIN USERSROLES AS UR\
                                                ON U.UserID = UR.UserID\
                                            WHERE U.UserID = {};'.format(member.id))
                        
                        dbRoles = self.cursor.fetchall()
                        dbRolesList = []
                        for role in dbRoles:
                            dbRolesList.append(role[0])
                        

                        memberRoles = []
                        for role in member.roles:
                            memberRoles.append(role.id)
                        

                        for memberRole in memberRoles:
                            if memberRole in allRoles:
                                if memberRole not in dbRolesList:
                                    try:
                                        role = guild.get_role(memberRole)
                                        await self.insert_users_role(member, role)
                                    except Exception as err:
                                        print(err)

                        for dbRole in dbRolesList:
                            if dbRole not in memberRoles:
                                role = guild.get_role(dbRole)
                                await self.remove_users_role(member, role)
                                   
                
                except MySQLdb.Error as err:
                    print(member.name + " not in the database")
                

    def cog_unload(self):
        self.detect_anomalies.cancel()

    @detect_anomalies.before_loop
    async def before_detect_anomalies(self):
        print('Database: Waiting...')
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Database(client))

