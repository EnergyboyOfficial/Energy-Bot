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

# List of dares
dares = [
    "Sing your favorite song out loud.",
    "Do your best impression of a famous celebrity.",
    "Send a funny meme to a random member in this server.",
    "Change your Discord nickname to 'Daredevil' for the next hour.",
    "Call a friend and tell them a ridiculous story to see if they believe it.",
    "Take a selfie and post it in the server's selfie channel.",
    # Add more dares here...
]

# List of truths
truths = [
    "What is your biggest fear?",
    "What is your favorite food?",
    "Have you ever had a crush on someone in this server?",
    "What is the most embarrassing thing that has happened to you?",
    "What is your hidden talent?",
    "Have you ever told a secret you promised to keep?",
    # Add more truths here...
]

# List of players for Spin the Bottle
spin_the_bottle_players = []

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

    if message.content.startswith('!truth'):
        truth = random.choice(truths)
        await message.channel.send(f"🤫 {message.author.mention}, here's your truth question: {truth}")

    if message.content.startswith('!dare'):
        dare = random.choice(dares)
        await message.channel.send(f"👀 {message.author.mention}, here's your dare challenge: {dare}")

    if message.content.startswith('!spinthebottle'):
        if message.author not in spin_the_bottle_players:
            spin_the_bottle_players.append(message.author)
            await message.channel.send(f"{message.author.mention} joined Spin the Bottle!")

    if message.content.startswith('!endspinthebottle'):
        if message.author in spin_the_bottle_players:
            spin_the_bottle_players.remove(message.author)
            await message.channel.send(f"{message.author.mention} left Spin the Bottle.")

        if len(spin_the_bottle_players) == 0:
            await message.channel.send("Spin the Bottle ended. No one is playing.")

    if message.content.startswith('!spinit'):
        if len(spin_the_bottle_players) < 2:
            await message.channel.send("Not enough players to spin the bottle.")
        else:
            bottle_spinned = random.sample(spin_the_bottle_players, 2)
            await message.channel.send(f"🍾 Bottle spinned! {bottle_spinned[0].mention} and {bottle_spinned[1].mention}, it's your turn! 🍾")

# Run the bot with your token
bot.run('Bot-Token-Here')
