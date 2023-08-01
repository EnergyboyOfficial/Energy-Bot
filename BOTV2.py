import discord
import psutil
import random
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with the token you got from the Discord Developer Portal
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Fun Commands

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name='stats')
async def stats(ctx):
    system_stats = get_system_stats()
    await ctx.send(system_stats)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! :ping_pong:')

@bot.command(name='echo')
async def echo(ctx, *, message):
    await ctx.send(message)

@bot.command(name='roll')
async def roll(ctx, dice: str):
    try:
        num, sides = map(int, dice.split('d'))
        rolls = [random.randint(1, sides) for _ in range(num)]
        total = sum(rolls)
        await ctx.send(f"Rolls: {', '.join(map(str, rolls))}\nTotal: {total}")
    except Exception as e:
        await ctx.send("Invalid input. Use the format `!roll XdY` where X is the number of dice and Y is the number of sides.")

@bot.command(name='coinflip')
async def coinflip(ctx):
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(result)

# Moderation Commands

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided."):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked from the server. Reason: {reason}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick members.")
    except discord.HTTPException:
        await ctx.send("Failed to kick the member. Please try again later.")

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided."):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned from the server. Reason: {reason}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban members.")
    except discord.HTTPException:
        await ctx.send("Failed to ban the member. Please try again later.")

@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, member_id: int):
    banned_users = await ctx.guild.bans()
    for banned_entry in banned_users:
        user = banned_entry.user
        if user.id == member_id:
            try:
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name} has been unbanned from the server.')
                return
            except discord.Forbidden:
                await ctx.send("I don't have permission to unban members.")
            except discord.NotFound:
                await ctx.send("User not found in the ban list.")
            except discord.HTTPException:
                await ctx.send("Failed to unban the user. Please try again later.")
            break
    else:
        await ctx.send("User not found in the ban list.")

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'{len(deleted) - 1} messages have been deleted.')
    except discord.Forbidden:
        await ctx.send("I don't have permission to manage messages.")
    except discord.HTTPException:
        await ctx.send("Failed to delete messages. Please try again later.")

# Auto-Moderation

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    caps_percentage = sum(1 for char in message.content if char.isupper()) / len(message.content)
    if caps_percentage > 0.7:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please avoid excessive use of caps.")

    bad_words = ["badword1", "badword2", "badword3"]
    if any(word in message.content.lower() for word in bad_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please refrain from using inappropriate language.")

    await bot.process_commands(message)

def get_system_stats():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    network = psutil.net_io_counters()
    network_usage = f"Upload: {convert_bytes(network.bytes_sent)} / Download: {convert_bytes(network.bytes_recv)}"

    return f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}%\nDisk Usage: {disk_usage}%\nNetwork Usage: {network_usage}"

def convert_bytes(bytes):
    sizes = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024
        i += 1
    return f"{bytes:.2f} {sizes[i]}"

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')
