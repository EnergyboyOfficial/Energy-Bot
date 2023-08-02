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

    if message.content.startswith('!truth'):
        truths = [
            "What is your biggest fear?",
            "What is your favorite food?",
            "Have you ever had a crush on someone in this server?",
            "What is the most embarrassing thing that has happened to you?",
            "What is your hidden talent?",
            "Have you ever told a secret you promised to keep?",
            "If you could switch lives with someone for a day, who would it be?",
            "What is the last thing you searched for on the internet?",
            "Have you ever been in love?",
            "What is the one thing you wish you could change about yourself?",
            "What is your dream job?",
            "If you could time travel, what time period would you visit?",
            "Have you ever cheated on a test?",
            "What is your biggest pet peeve?",
            "What is the craziest thing you've ever done?",
            "If you could have one superpower, what would it be?",
            "Have you ever had a crush on someone in this server?",
            "What is your most embarrassing moment?",
            "If you could switch lives with someone for a day, who would it be?",
            "Have you ever had a crush on someone in this server?",
            # Add more truth questions here
        ]
        truth = random.choice(truths)
        await message.channel.send(f"🤫 {message.author.mention}, here's your truth question: {truth}")

    if message.content.startswith('!dare'):
        dares = [
            "Show your best dance moves!",
            "Send a selfie with a funny face!",
            "Do your best impression of a famous celebrity.",
            "Sing a random song out loud.",
            "Send a flirty message to someone in this server.",
            "Change your Discord nickname to 'Daredevil' for the next hour.",
            "Call a friend and tell them a ridiculous story to see if they believe it.",
            "Take a selfie and post it in the server's selfie channel.",
            "Show your most embarrassing photo!",
            "Send a message in the server's general chat saying 'I love this server!'",
            "Do 10 jumping jacks in front of your camera.",
            "Confess your secret crush in the server's secret-confessions channel.",
            "Try to do a handstand and show your attempt on camera.",
            "Write a short poem and share it with the server.",
            "Do an impression of your favorite animal.",
            "Do a funny catwalk and strut your stuff.",
            "Tell a funny joke to the server.",
            "Do your best impression of a famous YouTuber.",
            "Sing 'Happy Birthday' to a random server member.",
            "Send a heartwarming message to someone you appreciate in the server.",
            # Add more dare challenges here
        ]
        dare = random.choice(dares)
        await message.channel.send(f"👀 {message.author.mention}, here's your dare challenge: {dare}")

# Run the bot with your token
bot.run('Bot-Token-Here')
