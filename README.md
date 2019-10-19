# FIT-Community-Discord-Bot


## moderatorUser

`async def add_member(self, ctx, member: discord.Member, userIndex)`
* add member to database (test for adding same index)

`async def set_index(self, ctx, member: discord.Member, userIndex)`
* change index of member in database

`async def set_status(self, ctx, member: discord.Member, status, option)`
* set status of member
    * option: '-d' - discord status (Active/Left/Kicked/Banned)
    * option: '-f' - fakultet status (Aktivan/Napustio/Zaledio)

`async def add_role(self, ctx, member: discord.Member, *roles: discord.Role):`
* update database UserRole (ToDo)

`async def remove_role(self, ctx, member: discord.Member, *roles: discord.Role)`
* update database UserRole (ToDo)

`async def set_name(self, ctx, member: discord.Member, *name)`
* updates database

`async def kick(self, ctx, member: discord.Member, reason = None):`
* kick member from server
* change discord status to kicked (ToDo)

`async def ban(self, ctx, member: discord.Member, reason = None)`
* ban member from server
* change discord status to banned (ToDo)

## moderatorMsg

`async def purge(self, ctx, numberOfMessages = 1)`
* delete n number of messages
* default n = 1

`async def echo(self, ctx, channel, *, message)`
* write message as bot to a specific channel

`async def edit(self, ctx, channel, id: int, *, newMessage)`
* edit bots message in specific channel
* enable developer options in order to copy message ID

`async def move(self, ctx, oldChannel, id: int, newChannel, option = None)`
* moves message from channelA to channelB in form of an embed
* if option --delete or -d, deletes message after move


