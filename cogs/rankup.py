import discord
from discord.ext import commands
from discord.ext import tasks

from models.role import Role
from models.user import users_roles_association
from models.user import User

from utils import misc

class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

class Tree:
    def __init__(self):
        self.root = None
        # self.cmp = lambda value, node: value < node.value

    def setCmpFunction(self, function):
        self.cmp = function

    def GetRoot(self):
        return self.root

    def GetLeftChild(self, node):
        return node.left if node is not None else None

    # def GetRightChild(self, node):
    #     return node.right if node is not None else None

    def add(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)
    
    def _add(self, value, node):
        
        if value.Value < node.value.Value == True:
            if node.left is not None:
                self._add(value, node.left)
            else:
                print(value.Name + " added left " + node.value.Name)
                node.left = Node(value)
        else:
            if node.right is not None:
                self._add(value, node.right)
            else:
                print(value.Name + " added right " + node.value.Name)
                node.right = Node(value)
    
    def find(self, value):
        if self.root is not None:
            self._find(value, self.root)
        else:
            return None

    def _find(self, value, node):
        if value.Value == node.value.Value:
            return node
        elif value.Value < node.value.Value and node.left is not None:
            return self._find(value, node.left)
        elif value.Value > node.value.Value and node.right is not None:
            return self._find(value, node.right)
        else:
            return None

    

class Rankup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.roleName = "Registrovan";
        self.role = None
        self.roleTree = None

    def SetRole(self):
        if self.role is None:
            self.role = misc.getRoleByName(self.client, self.roleName)

    def SetValue(self, role: Role):
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()

            if role.ParentRole is not None:
                parent = session.query(Role) \
                    .filter(Role.RoleId == role.ParentRole) \
                    .one()
                
                children = session.query(Role) \
                    .filter(Role.ParentRole == role.ParentRole) \
                    .count()

                role.Value = parent.Value + 1 + children * 0.1
            else:
                role.Value = 0
    
    def CreateTree(self):
        if self.roleTree is None:
            database = self.client.get_cog("Database")
            if database is not None:
                session = database.Session()
                rankedRoles = session.query(Role) \
                        .filter(Role.ParentRole != None) \
                        .all()

                rootRole = session.query(Role) \
                        .filter(Role.RoleId == 440055845552914433) \
                        .one()

                RoleTree = Tree()
                #RoleTree.setCmpFunction(lambda rankedRole, node: rankedRole.Value < node.value.Value)
                RoleTree.add(rootRole)
                for rankedRole in rankedRoles:
                    print(rankedRole)
                    RoleTree.add(rankedRole)

                return RoleTree
        
        return None
        
        
    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def connect(self, ctx, parentRole: discord.Role, childRole: discord.Role):
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()
            parent = session.query(Role) \
                .filter(Role.RoleId == parentRole.id) \
                .one_or_none()

            child = session.query(Role) \
                .filter(Role.RoleId == childRole.id) \
                .one_or_none()

            if parent is not None and child is not None:
                child.ParentRole = parent.RoleId
                self.SetValue(child)
                session.commit()

            session.close()

    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def imatrikulant(self, ctx):
        self.SetRole()
        await ctx.author.add_roles(self.role)
        # embed

    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def apsolvent(self, ctx):
        self.SetRole()
        await ctx.author.add_roles(self.role)
        # embed

    
    @commands.command(aliases=["diplomirao", "diplomirala"])
    @commands.has_any_role('Administrator') 
    async def diploma(self, ctx):
        self.SetRole()
        await ctx.autor.kick(reason = "Diplomirao/Diplomirala")
        # update fakultet status
        # embed

    
    @commands.command(aliases=["alumni", "alumna"])
    @commands.has_any_role('Administrator') 
    async def alum(self, ctx):
        self.SetRole()
        alumRole = misc.getRoleByName(self.client, "Alumni")
        pass
    
    
    @commands.command(aliases=["ocistio", "ocistila"])
    @commands.has_any_role('Administrator') 
    async def cista(self, ctx):
        self.SetRole()
        # see current role
        # get higher role
        # add higher role
        # remove lower role
        pass

    
    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def uslov(self, ctx):
        self.SetRole()
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()

            roles = ctx.author.roles
            rankedRoles = session.query(Role) \
                .join(users_roles_association) \
                .filter(Role.ParentRole != None) \
                .filter(users_roles_association.c.UserId == ctx.author.id) \
                .all()
                
            # for role in roles not in rankedRoles:
            #     roles.remove(role)
            # for role in rankedRoles:
            #     print(role.Name)

            # rankedRolesIDs = [role.RoleId for role in rankedRoles]
            # usersRankedRoles = [role for role in roles if role.id in rankedRolesIDs]

            # for role in usersRankedRoles:
            #     print(role.name)
            xRole = self.findHighestRole(rankedRoles)
            await ctx.send(xRole.Name)
        # see current role
        # get higher role
        # add the higher role
        pass

    @commands.command(aliases=["obnovio", "obnovila"])
    @commands.has_any_role('Administrator') 
    async def obnova(self, ctx):
        self.SetRole()
        await ctx.author.add_roles(self.role)
        # embed

    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def kolizija(self, ctx):
        self.SetRole()
        await ctx.send(self.role)
        # embed

    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def ispis(self, ctx):
        await ctx.autor.kick(reason = "Ispis")
        # update fakultet status
        # embed

    def findHighestRole(self, roles: []):
        if self.roleTree is None:
            self.roleTree = self.CreateTree()
            print(self.roleTree.root.left.value.Name)
        roles.sort(key = lambda x: x.Value, reverse = True)
        for role in roles:
            node = self.roleTree.find(role)
            print(node)
            if node is not None:
                print(node)
                leftChild = self.roleTree.GetLeftChild(node.left)
                if leftChild is not None:
                    return leftChild
        return None


def setup(client):
    client.add_cog(Rankup(client))