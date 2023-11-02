import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import logging

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True
intents.members = True
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='/clan ', intents=intents, case_sensitive=False) 

clan_data = {}  # Store data for each clan {clan_creator_id: [clan_name, channel_id, role_id, members_list]}
invite_data = {}
owner_id = 525083106093563929 #Your user id (needed to run sync)
guild_id = 1159153096191123517 #Your server id
clan_owner_role_name = "[TEAM LEADER]"
show_clan_owner_seperate = True


#/clan create {clan name}
@bot.tree.command(name="clan-create", description="Create a new clan")
async def create(ctx, name: str):
    if len(name) >= 5:
        await ctx.response.send_message("Clan names must be 5 characters or less.")
        return

    if ctx.user.id in clan_data:
        await ctx.response.send_message("You are already own a clan you cannot create a new one.")
        return
    
    for value in clan_data.values():
        if ctx.user.id in value[3]:
            await ctx.response.send_message("You are already in a clan you cannot create a new one.")
            return

    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.user: discord.PermissionOverwrite(read_messages=True)
    }
    category = discord.utils.get(guild.categories, name="Clan Category")
    if category is None:
        category = await guild.create_category(name="Clan Category")

    clan_owner_role = discord.utils.get(guild.roles, name=clan_owner_role_name)
    if clan_owner_role is None:
        clan_owner_role = await guild.create_role(name=clan_owner_role_name, mentionable=True, hoist = show_clan_owner_seperate)

    channel = await category.create_text_channel(name, overwrites=overwrites)
    role = await guild.create_role(name=name)
    await ctx.user.add_roles(role)
    await ctx.user.add_roles(clan_owner_role)
    await channel.set_permissions(role, read_messages=True)
    await ctx.response.send_message(f'Clan {name} created!')

    clan_data[ctx.user.id] = [name, channel.id, role.id, []]

#/clan invite {@user}
@bot.tree.command(name="clan-invite", description="Invite a user to your clan")
async def invite(ctx, user: discord.User):
    if ctx.user.id not in clan_data:
        await ctx.send("You are not in any clan. Create a clan first.")
        return

    clan_creator_id = ctx.user.id
    if clan_creator_id not in clan_data:
        await ctx.response.send_message("Only the clan creator can invite users.")
        return

    clan_name, channel_id, role_id, member_list= clan_data[clan_creator_id]
    embed = discord.Embed(
        title=f"{clan_name}",
        description=f"You have been invited to {clan_name} by {ctx.user.name}",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=ctx.guild.icon.url)

    view = MyView()

    await user.send(embed=embed, view=view)
    await ctx.response.send_message(f"Invite sent!")

    invite_data[user.id] = ctx.user.id

#/clan disband {clan name}
@bot.tree.command(name="clan-disband", description="Delete your clan channel and role")
async def disband(ctx):
    if ctx.user.id not in clan_data:
        await ctx.response.send_message("You do not own a clan to disband.")
        return

    clan_creator_id = ctx.user.id
    if ctx.user.id != clan_creator_id:
        await ctx.response.send_message("Only the clan creator can disband the clan.")
        return

    clan_name, channel_id, role_id, member_list = clan_data[clan_creator_id]
    guild = ctx.guild
    role = discord.utils.get(guild.roles, id=role_id)
    channel = discord.utils.get(guild.channels, id=channel_id)

    if role is not None:
        await role.delete()
        await ctx.response.send_message("Role deleted.")
    elif role is None:
        await ctx.response.send_message("No role found.")
        
    if channel is not None:
        await channel.delete()

    ctx.response.send_message(f'Clan {clan_name} disbanded.')
    del clan_data[clan_creator_id]

#/clan kick {@user}
@bot.tree.command(name="clan-kick", description="Kick a user from your clan")
async def kick(ctx, user: discord.User):
    if ctx.user.id not in clan_data:
        await ctx.response.send_message("You do not own a clan to kick members.")
        return

    guild = bot.get_guild(guild_id)
    member = guild.get_member(user.id)
    clan_members = clan_data[ctx.user.id][3]
    if user.id in clan_members:
        role_id = clan_data[ctx.user.id][2]
        role = guild.get_role(role_id)
        await member.remove_roles(role)
        clan_data[ctx.user.id][3].remove(user.id)
        await ctx.response.send_message(f'{member.mention} has been kicked from the clan.')
    else:
        await ctx.response.send_message(f'{member.mention} is not a member of your clan.')

#/clan leave
@bot.tree.command(name="clan-leave", description="Leave the clan you're in")
async def leave(ctx):
    for key, value in clan_data.items():
        if ctx.user.id == key:
            await ctx.response.send_message("You own a clan and cannot leave. Please disband the clan.")
            return
        
    clan_creator_id = None
    for key, value in clan_data.items():
        if ctx.user.id in value[3]:
            clan_creator_id = key
            break
    if clan_creator_id is not None:
        role_id = clan_data[clan_creator_id][2]
        role = ctx.guild.get_role(role_id)
        await ctx.user.remove_roles(role)
        clan_data[clan_creator_id][3].remove(ctx.user.id)
        await ctx.response.send_message(f"You have left the clan.")
    else:
        await ctx.response.send_message("You are not a member of any clan.")

@bot.tree.command(name="clan-color", description="Chane your clan role color.")
async def color(ctx, hex_code: str):
    if ctx.user.id in clan_data:
        guild = ctx.guild
        role = guild.get_role(clan_data[ctx.user.id][2])
        if role:
            try:
                color = discord.Color(int(hex_code, 16))
                await role.edit(color=color)
                await ctx.response.send_message(f"Color for the clan {role.name} has been set to {hex_code}")
            except ValueError:
                await ctx.response.send_message("Invalid hex code provided.")
        else:
            await ctx.response.send_message("Clan role not found.")
    else:
        await ctx.response.send_message("Only the clan owner can use this command")

@bot.command()
async def sync(ctx):
    if ctx.author.id == owner_id:
        await bot.tree.sync()
        await ctx.send("Commands synced")
    else:
        await ctx.send("Only the server owner can use this command")

@bot.command()
async def ownercolor(ctx, hex_code: str):
    if ctx.author.id == owner_id:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=clan_owner_role_name)
        if role:
            try:
                color = discord.Color(int(hex_code, 16))
                await role.edit(color=color)
                await ctx.send(f"Color for {role.name} role has been set to {hex_code}")
            except ValueError:
                await ctx.send("Invalid hex code provided.")
        else:
            await ctx.send("Role not found.")
    else:
        await ctx.send("Only the server owner can use this command")

@bot.event
async def on_ready():
    bot.add_view(MyView())
    
class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.green, label="Accept", custom_id="join")
    async def handle_accept(self, interaction:discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = bot.get_guild(guild_id)
        clan_creator_id = None
        for key, value in clan_data.items():
            if value[0] == interaction.message.embeds[0].title:
                clan_creator_id = key
                break
        if clan_creator_id is not None:
            role_id = clan_data[clan_creator_id][2]
            role = guild.get_role(role_id)
            member = guild.get_member(user.id)
            if role is not None and member is not None:
                clan_data[clan_creator_id][3].append(user.id)
                await member.add_roles(role)
                await interaction.response.send_message("You have accepted the invitation.", ephemeral=True)
                if user.id in invite_data:
                    del invite_data[user.id]
            else:
                await interaction.response.send_message(f"Role not found! role: {role} and member: {member}", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid Invitation!", ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.red, label="Reject", custom_id="reject")
    async def handle_reject(self, interaction:discord.Interaction, button: discord.ui.Button): 
        original_author_id = invite_data.get(interaction.user.id)
        guild = bot.get_guild(guild_id)
        if original_author_id:
            guild = bot.get_guild(guild_id)
            original_author = guild.get_member(original_author_id)
            await interaction.response.send_message("You have rejected the invite.", ephemeral=True)
            if original_author:
                await original_author.send(f"{interaction.user} has declined the invite.")
            else:
                logging.warning(f"Original author not found for user ID: {original_author_id}")
            if interaction.user.id in invite_data:
                del invite_data[interaction.user.id]
        else:
            logging.warning("Original author ID not found for the rejected invite.")



bot.run('MTE2Mzg5NjM3Njc3NDYzNTU4MQ.GZqDrM.ZYr2bOz_82Qd4GbPrUT2MiiuYV0xiZiSTKcEMI') #REPLACE WITH YOUR BOT TOKEN, INSIDE THE ' '
