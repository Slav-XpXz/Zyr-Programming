from distutils.command.check import check
import time
import aiohttp
from webserver import keep_alive
import os
import discord
import asyncio
import random
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
client = commands.Bot(command_prefix='$', intents=intents)
statuses=['League Of Legends', 'Fortnite', 'Valorant', 'Minecraft', 'Roblox', 'with my pussy', 'with nukes', 'Finding My Father Simulator', 'Getting A Life Simulator', 'Getting Bitches Simulator']

@client.event
async def on_ready():
  print('Bot is online...')
  while True:
    for x in statuses:
      await client.change_presence(status=discord.Status.online, activity=discord.Game(x))
      await asyncio.sleep(69)
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
      embed = discord.Embed(title = "Error", color = 0xfcf528)
      embed.add_field(name = "Permission Missing", value = "You don't have permission to do this, retard.")
      embed.set_footer(text = f'Requested by {ctx.message.author}', icon_url = ctx.author.display_avatar)
      await ctx.send(embed=embed)
    elif isinstance(error,commands.MissingRequiredArgument):
      embed = discord.Embed(title = "Error", color = 0xfcf528)
      embed.add_field(name = "Arguments Missing", value = "Are you so stupid that you can't run a fucking command?")
      embed.set_footer(text = f'Requested by {ctx.message.author}', icon_url = ctx.author.display_avatar)
      await ctx.send(embed=embed)


@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)  
async def kick(ctx, member : discord.Member, *, reason=None):
  embed = discord.Embed(title = "User Was Kicked From Server", color = 0xf03524)
  embed.add_field(name = "User Kicked", value = str(member))
  embed.add_field(name = "Reason for Kick", value = reason + ' L Bozo + Ratio') #TODO fix it if theres no reason
  embed.set_footer(text = f'Kicked by {ctx.message.author}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed = embed)
  await member.send('You have been kicked from Zyr Programming Language for:' + reason)
  await member.kick(reason=reason)



@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason=None):
  embed = discord.Embed(title = "User Was Banned From Server", color = 0xcf2376)
  embed.add_field(name = "User Banned", value = str(member))
  embed.add_field(name = "Reason for Ban", value = reason + ' L Bozo + Ratio') #TODO fix it if theres no reason
  embed.set_footer(text = f'Banned by {ctx.message.author}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed = embed)
  await member.send('You have been banned from Zyr Programming Language for:' + reason)
  await member.ban(reason=reason)





@client.command()
@commands.has_permissions(manage_messages = True)
async def warn(ctx, member : discord.Member, *, reason=None):
  await member.send(f'you were warned in Zyr Programming Language for: {reason}')
  embed = discord.Embed(title = "User Warned", color = 0xfcc028)
  embed.add_field(name = str(member), value = 'Warning: ' + reason + ' L Bozo + Ratio') #TODO fix it if theres no reason
  embed.set_footer(text = f'Warned by {ctx.message.author}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed = embed)



@client.command(aliases=["userinfo"])
async def whois(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
      member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.dark_purple(), timestamp=ctx.message.created_at, title=f"User Info - {member}")
    embed.set_thumbnail(url=member.display_avatar)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)

    embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.display_avatar)
    print(member.top_role.mention)
    await ctx.send(embed=embed)


@client.command(aliases=['m'])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
	embed = discord.Embed(title = "User Muted", color = 0xFFC600)
	embed.add_field(name = str(member), value = 'Muted: ' + reason + ' L Bozo + Ratio') #TODO fix it if theres no reason
	embed.set_footer(text = f'Muted by {ctx.message.author}', icon_url = ctx.author.display_avatar)
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")
	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")
		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
		await member.add_roles(mutedRole, reason=reason)
		await member.send(f"You were muted in Zyr Programming Language for: {reason}")
		await ctx.send(embed = embed)



@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
	await member.remove_roles(mutedRole)
	embed = discord.Embed(title = "User Unmuted", color = 0x72FF1F)
	embed.add_field(name = str(member), value = "Welcome back, try not to get muted again dumbfuck.")
	embed.set_footer(text=f'Unmuted by {ctx.message.author}', icon_url = ctx.author.display_avatar)
	await member.send(f"You were unmuted in Zyr Programming Language.")

@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx,limit: int):
	if limit>100:
		embed = discord.Embed(title = "Error", color = 0xfcf528)
		embed.add_field(name = "Impossible", value = "The limit is 100, I can't delete more lmfao")
		embed.set_footer(text = f'Requested by {ctx.message.author}', icon_url = ctx.author.display_avatar)
		await ctx.send(embed=embed)
		return
	await asyncio.sleep(2)
	await ctx.channel.purge(limit=limit)
	await ctx.send(f"purged by {ctx.message.author.mention}")
	time.sleep(2)
	await ctx.message.delete()

@client.command(aliases=['av'])
async def avatar(ctx, member: discord.Member = None):
  if not member:
    member = ctx.message.author

  embed = discord.Embed(title = "Ugly Ass Avatar of " + str(member), colour=discord.Colour.dark_purple())
  embed.set_image(url=member.display_avatar)
  embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed=embed)


@client.command(aliases=['git'])
async def github(ctx):
  await ctx.send("https://github.com/Slav-XpXz")

@client.command()
async def zyr(ctx):
  await ctx.send("https://github.com/Slav-XpXz/Zyr")

@client.command()
async def patreon(ctx):
  await ctx.send("https://www.patreon.com/slav_XpXz")

@client.command()
async def pugno(ctx):
	await ctx.send("Yeah ikr he's the best.")

@client.command()
async def mwa(ctx):
	i = random.randint(1, 100)
	if i < 100:
		await ctx.send("wtf did you just say to me little bitch.")
	else:
		await ctx.send('😏')




@client.command()
async def kiss(ctx, member: discord.Member = None):
  if not member:
    await ctx.send(f'{ctx.message.author.mention} so lonely trying to kiss your self :skull:')
  else:
    await ctx.send(f'{ctx.message.author.mention} kissed {member.mention} pretty sexy')



@client.command()
async def colourchroma(ctx, member: discord.Member = None):
  if not member:
    member = ctx.message.author
  await member.edit(nick="Colourchroma")
  await ctx.send(f'Synth 2.0 that you?! {member.mention}')


@client.command(alias=['n'])
async def nick(ctx, member: discord.Member = None, *, nick):
  await member.edit(nick=nick)
  await ctx.send(f"Set {member.mention}'s nickname to {nick}")


@client.command()
async def ineedhelp(ctx):
  await ctx.send("I'd rather play Visual Studio Code retard")





@client.command()
async def meme(ctx):
  embed = discord.Embed(title="Dumb Fuck Shitpost", color = 0x0876DF)
  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
        res = await r.json()
        embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed)



@client.command()
async def sex(ctx, member: discord.Member = None):
  if not member or ctx.message.author == member:
    await ctx.send(f'{ctx.message.author.mention}, nobody wants to see you jerk off. Please kys.')
  else:
    try:
      await ctx.send("Dom or Sub?")
      def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel
      msg = await client.wait_for('message', check = check, timeout=21)
    except asyncio.TimeoutError:
      await ctx.send('Are you fucking retarded? Try being faster at typing. You got legit 21 seconds to type 3 letters mf.')
    else:
      if msg.content.lower() == 'dom':
        await ctx.send(f'{ctx.message.author} dommed {str(member)}, kinda hot ngl.')
      elif msg.content.lower() == 'sub':
        await ctx.send(f'{ctx.message.author} got dommed by {str(member)}, kinda hot ngl.')
      else:
        await ctx.send('Are you fucking retarded? I gave you two fucking options that you could have copy pasted smh.')

@client.command(aliases=['8ball', 'magicball'])
async def magic8ball(ctx, * question):
  if not question:
    await ctx.send('Tf is your question?')
  responses = ['hell no, wtf?', 'bro stfu the answer is no, retard', 'no, plain and simple', 'dumbfuck, you already know the answer is no', 'yes daddy', 'yessir', 'yes, mf you should know this', 'although you may be bitchless, yes', 'maybe', 'idk tbh why you talking to an inanimate object', 'give nitro for answer', "could you repeat that? i can't hear you cuz ur such a squeaker"]
  if question:
    await ctx.send(random.choice(responses))

TOKEN = os.environ['token']
keep_alive()
client.run(TOKEN)
