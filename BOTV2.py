import discord
import psutil
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

# Replace 'YOUR_BOT_TOKEN' with the token you got from the Discord Developer Portal
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to get system stats
def get_system_stats():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    network = psutil.net_io_counters()
    network_usage = f"Upload: {convert_bytes(network.bytes_sent)} / Download: {convert_bytes(network.bytes_recv)}"

    return f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}%\nDisk Usage: {disk_usage}%\nNetwork Usage: {network_usage}"

# Function to convert bytes to a more human-readable format
def convert_bytes(bytes):
    sizes = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024
        i += 1
    return f"{bytes:.2f} {sizes[i]}"

# Slash command for /hello
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

# Slash command for /stats
@bot.command(name='stats')
async def stats(ctx):
    system_stats = get_system_stats()
    await ctx.send(system_stats)

# Event handler for when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Run the bot with your token
bot.run('YOUR_BOT_TOKEN')
