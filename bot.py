import discord
import psutil
import random

intents = discord.Intents.default()
intents.message_content = True

# Replace 'YOUR_BOT_TOKEN' with the token you got from the Discord Developer Portal
bot = discord.Client(intents=intents)

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

# Event handler for when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Event handler for when a message is received
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('!stats'):
        system_stats = get_system_stats()
        await message.channel.send(system_stats)
    
    if message.content.startswith('!flip'):
        coin_flip = 'Heads' if random.randint(0, 1) == 0 else 'Tails'
        await message.channel.send(f"The coin landed on: {coin_flip}")
    
    if message.content.startswith('!ping'):
        latency = bot.latency
        await message.channel.send(f"Pong! Latency: {latency*1000:.2f} ms")

    if message.content.startswith('!lovecalc'):
        try:
            user_mentions = message.mentions
            if len(user_mentions) < 2:
                raise ValueError("Please mention two users for love calculation.")
            
            random.seed(user_mentions[0].id + user_mentions[1].id)
            love_percentage = random.randint(0, 100)
            
            await message.channel.send(f"💘 {user_mentions[0].mention} and {user_mentions[1].mention}'s love percentage is {love_percentage}%!")
        except ValueError as e:
            await message.channel.send(str(e))

# Run the bot with your token
bot.run('Bot-Token-Here')
