import discord
from discord.ext import commands
import discord, datetime, time
from discord_buttons_plugin import *
from secret import TOKEN
import requests



bot = commands.Bot(command_prefix=commands.when_mentioned_or("_"), intents=discord.Intents.all())
bot.remove_command("help")
buttons = ButtonsClient(bot)

@bot.event
async def on_ready():
  print("Chad's Ready To Go Bitch!")
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Your Girl"))





start_time = time.time()
@bot.command(pass_context=True)
async def uptime(ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Bot Uptime", value=text)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)



@bot.command()
async def help(ctx):
  em = discord.Embed(title = "Bot commands!", description="All Commands For The Bot:", color=0x00ffe1)
  em.add_field(name="Latency/Ping", value = "`_latency`", inline = False)
  em.add_field(name="User Id", value = "`_myid or _myid {user}`", inline = False)
  em.add_field(name="Dm", value = "`_dm {user} {content}`", inline = False)
  em.add_field(name="Modmail", value = "`_mm {mod} {content}`", inline = False)
  em.add_field(name="Profile Picture", value = "`_pfp or _pfp {user}`", inline = False)
  em.add_field(name="About", value = "`_aboutme or _aboutme {user}`", inline = False)
  em.add_field(name="Clear", value = "`_clear {amount of messages to clear}`", inline = False)
  em.add_field(name="Cats", value = "`_cats`", inline = False)
  em.add_field(name = "Prefix", value = "My Prefix Is `_` (UnderScore)", inline=False)
  await ctx.channel.send(embed=em)

@bot.command()
async def myping(ctx):
  await ctx.channel.send("My Latency Is " + str(bot.latency*1000) + "ms")
	
@bot.command()
async def myid(ctx, member: discord.Member=None):
  member = member or ctx.author
  await ctx.channel.send(f"ID Of {member.display_name}: `{member.id}`")



@bot.command(aliases=["dmmtheguy"])
async def dm(ctx, member:discord.Member, *, content):
  em = discord.Embed(title="New Dm You Got There!")
  em.add_field(name="Content: ", value = content)
  em.set_footer(text=f"Message From {ctx.author}", icon_url=ctx.author.avatar_url)

  await member.send(embed=em)
  ctx.channel.send("Sent!")

@bot.command(aliases=["mm", "dmmod"])
async def modmail(ctx, member:discord.Member, *, content):
  em = discord.Embed(title="New Modmail!")
  em.add_field(name="Content: ", value = content)
  em.set_footer(text=f"Message From {ctx.author}", icon_url=ctx.author.avatar_url)

  await member.send(embed=em)


@bot.command(aliases=["profilepic"])
async def pfp(ctx, member: discord.Member=None):
  member = member or ctx.author
  em = discord.Embed(color = member.color, timestamp = ctx.message.created_at)
  em.set_thumbnail(url=member.avatar_url)

  await ctx.channel.send(embed=em)



@bot.command(aliases=["about", "spy", "profile"])
async def aboutme(ctx, member: discord.Member=None):
  member = member or ctx.author
  
  roles = member.roles
  em = discord.Embed(color = member.color, timestamp=ctx.message.created_at)

  em.set_author(name=f"User Info - {member}")
  em.set_thumbnail(url=member.avatar_url)
  em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

  em.add_field(name="ID: ", value = member.id)
  em.add_field(name="Guild Game: ", value=member.display_name)

  em.add_field(name="Created At: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))
  em.add_field(name="Joined at: ", value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))

  em.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))

  em.add_field(name="Top role: ", value=member.top_role.mention)

  await ctx.channel.send(embed=em)

  
@bot.command()
async def yt(ctx):
	await buttons.send(
		content = "Imagine Not Subscribing", 
		channel = ctx.channel.id,
		components = [
			ActionRow([
				Button(
					label="My Youtube!", 
					style=ButtonType().Link,
          url = "https://www.youtube.com/channel/ItsSB"          
				)
			])
		]
	)
	
# Moderation

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, limit: int):
  if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=limit+1)
        await ctx.send(f'{limit} Messages Cleared by {ctx.author.mention}', delete_after=3)
  else:
    ctx.channel.send(f"{ctx.author.mention}, You don't have the needed permission")


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def webhook(ctx, webhook_url=None, *, contents: str):
  url = webhook_url or None
  if url == webhook_url:
    await ctx.channel.purge(limit=1)

    data = {"content": contents}
    requests.post(url, json=data)
  elif url == None:
    await ctx.channel.send("Please provide a webhook url.")

@bot.command(aliases=["cat", "meow", "cutecats"])
async def cats(ctx):
  r = requests.get('http://aws.random.cat/meow')
  if r.status_code == 200:
      js = r.json()
      await ctx.channel.send(js['file'])


@bot.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, member: discord.Member=None, *, reason=None):
  member == None or member
  if member == None:
    await ctx.channel.send("You can't kick yourself chad")
  elif member == ctx.message.author:
    await ctx.channel.send("Can't Kick Yourself Chad")
  else:
    await member.kick(reason=reason)
    await ctx.channel.send(f'User {member} has kicked.')


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason=None):
  reason == reason or "For Being A Retard"
  member == None or member
  if member == None:
    await ctx.channel.send("You can't ban yourself chad")
  elif member == ctx.message.author:
    await ctx.channel.send("Can't Ban Yourself Chad")
  else:
    await member.ban(reason=reason)
    await ctx.channel.send(f'User {member} has banned, Reason: {reason}')

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")
  
  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.channel.send(f"Unbanned {user.name}#{user.discriminator}")


bot.run(TOKEN)
