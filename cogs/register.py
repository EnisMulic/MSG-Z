from discord.ext import commands

class Register(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def register(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command passed...')

    @register.command()
    async def name(self, ctx, *, name):
        await ctx.send(f'Your name is {name}')

    @register.command()
    async def index(self, ctx, index):
        await ctx.send(f'Your name is {index}')

    @register.command()
    async def roles(self, ctx, *, roles):
        user_roles = roles.split()
        await ctx.send(f'Your roles are {[role for role in user_roles]}')

    @register.command()
    async def image(self, ctx, *, image):
        await ctx.send(f'Image: {image}')

    @register.command()
    async def done(self, ctx):
        await ctx.send(f'DONE!!')
      

def setup(client):
    client.add_cog(Register(client))