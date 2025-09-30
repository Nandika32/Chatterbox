import os
from dotenv import load_dotenv
load_dotenv()
TOKEN =
os.getenv('DISCORD_BOT_TOKEN')
import discord
from discord.ext import commands
import random
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$',intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
@bot.command()
async def hello(ctx):
    """Sends a greeting message."""
    await ctx.send('Hello there!')    
@bot.command()
async def ping(ctx):
    """Checks the bot's latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')   
@bot.command()
async def say(ctx,*, message_to_say):
    """Makes the bot say something.
    Usage: $say [your message]"""
    await ctx.send(message_to_say)  
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}. Reason: {reason or "No reason provided."}')
    except discord.Forbidden:
        await ctx.send("I do not have the necessary permissions to kick this user.")
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command.")
@bot.command(name='8ball')
async def eight_ball(ctx, *, question: str):
    """Answers a yes/no question.
    Usage: $8ball [your question]"""
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don\'t count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Very doubtful.'
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
@bot.command()
async def info(ctx, member: discord.Member = None):
    """Displays information about a user.
    Usage: $info [optional: @user]"""
    if member is None:
        member = ctx.author 
    embed = discord.Embed(
        title=f"User Info for {member.name}",
        description=f"Here is some information about {member.mention}.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="ID", value=member.id, inline=False)
    
    embed.set_thumbnail(url=member.display_avatar.url)
    
    await ctx.send(embed=embed)
bot.run(TOKEN)
