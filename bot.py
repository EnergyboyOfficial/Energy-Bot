import discord
import psutil
import random

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

def get_system_stats():
    # Function to get system stats
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    network = psutil.net_io_counters()
    network_usage = f"Upload: {convert_bytes(network.bytes_sent)} / Download: {convert_bytes(network.bytes_recv)}"

    return f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}%\nDisk Usage: {disk_usage}%\nNetwork Usage: {network_usage}"

def convert_bytes(bytes):
    # Function to convert bytes to human-readable format
    sizes = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024
        i += 1
    return f"{bytes:.2f} {sizes[i]}"

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!stats'):
        system_stats = get_system_stats()
        await message.channel.send(system_stats)

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
            
            await message.channel.send(f"?? {user_mentions[0].mention} and {user_mentions[1].mention}'s love percentage is {love_percentage}%!")
        except ValueError as e:
            await message.channel.send(str(e))

    if message.content.startswith('!send_to_all'):
        if message.author.id == YOURUSERID:  # Replace 'YOUR_USER_ID' with your own Discord user ID
            args = message.content.split(' ', 1)
            if len(args) < 2:
                await message.channel.send("Please provide a message to send.")
                return

            all_guilds = bot.guilds
            for guild in all_guilds:
                channel = guild.text_channels[0]  # Change this to the channel where you want to send the message
                await channel.send(args[1])

    if message.content.startswith('!help'):
        help_message = """
        **Available Commands:**
        - !hello: Greet the bot
        - !stats: Show system stats
        - !ping: Check bot latency
        - !lovecalc @user1 @user2: Calculate love percentage between two users
        - !send_to_all <message>: Send a message to all servers the bot is in
        - !help: Show this help message
        """
        await message.channel.send(help_message)

bot.run('YOUR-BOT-TOKEN')
