import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from keep_alive import keep_alive
import os
from dotenv import load_dotenv

load_dotenv()
keep_alive()

print(type("ᴏᴘᴇɴ ꜱᴀʟᴏᴏɴ"))

TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("DISCORD_WELCOME_CHANNEL_ID")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

matricola_counter = 1 
ANIME_BACKGROUND = "ANIME_BACKGROUND.png"

def print_debug(message):
    print(f"\033[31m{message}\033[0m") 


@bot.event
async def on_ready():
    print_debug(f'✅ Bot connesso come {bot.user}')

@bot.event
async def on_member_join(member):
    global matricola_counter

    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).resize((100, 100))

    width , height = avatar.size

    widthAvatarInBg = int(width * 0.8)
    heightAvatarInBg = height

    avatar = avatar.resize((widthAvatarInBg, heightAvatarInBg))

    mask = Image.new("L", (100, 100), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 100, 100), fill=255)
    avatar = avatar.convert("RGBA")
    avatar.putalpha(mask)
    background = Image.open(ANIME_BACKGROUND).resize((400, 150))
    badge = Image.new("RGBA", (400, 200), (255, 255, 255, 0))
    badge.paste(background, (0, 0))
    badge = background.copy()

    draw = ImageDraw.Draw(badge)


    badgepath = f"badge_{member.id}.png"
    avatar_x = (badge.width - widthAvatarInBg) // 2  
    avatar_y = background.height 

    badge.paste(avatar, (avatar_x, avatar_y), avatar)
    
    print_debug(badgepath)
    badge.save(f"{badgepath}")

    matricola_counter += 1

    channel = bot.get_channel(int(WELCOME_CHANNEL_ID))

    if isinstance(channel, discord.TextChannel):
        print_debug(f"✅ Badge creato per {member.name}")
        await channel.send(f"🎉 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ꜱᴛʀ_ᴜɴɢʟᴇ {member.mention}",
                           file=discord.File(badgepath))
    else:
        print_debug(f"Errore: Il canale con ID {WELCOME_CHANNEL_ID} non è stato trovato o non è un canale di testo.")

if TOKEN:
    bot.run(TOKEN)
else:
    print_debug("Token non trovato!")
