import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from keep_alive import keep_alive
import os
from dotenv import load_dotenv

#LOADING ENV AND FLASK SERVER FUNCTION
load_dotenv()
keep_alive()

#INITILIZED DISCORD TOKEN AND PERMISSIONS 
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("DISCORD_WELCOME_CHANNEL_ID")
ANIME_BACKGROUND = "ANIME_BACKGROUND.png"

#BOT EVENT - BOT CONNECTION
@bot.event 
async def on_ready(): 
    print(f'✅ Bot connesso come {bot.user}')

#BOT EVENT - JOING MEMBER 
@bot.event
async def on_member_join(member):
    global matricola_counter

    #CREATION BADGE
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).resize((350, 150))
    background = Image.open(ANIME_BACKGROUND).resize((400, 150))
    badge = Image.new("RGBA" , (400 , 150))
    badge.paste(avatar , (0,0))
    badge.paste(background , (0,0) , background)
    badgepath = f"badge_{member.id}.png"
    badge.save(badgepath)

    #INITIALIZATION CHANNEL CONFIGURATION
    channel = bot.get_channel(int(WELCOME_CHANNEL_ID))
    if isinstance(channel, discord.TextChannel):
        print(f"✅ Badge creato per {member.name}")
        await channel.send(f"🎉 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ꜱᴛʀ_ᴜɴɢʟᴇ {member.mention}",
                           file=discord.File(badgepath))
    else:
        print(f"Errore: Il canale con ID {WELCOME_CHANNEL_ID} non è stato trovato o non è un canale di testo.")

#RUNNING BOT
if TOKEN:
    bot.run(TOKEN)
else:
    print("Token non trovato!")
