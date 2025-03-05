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

TOKEN = os.getenv("DISCORD_TOKEN")
WELCOME_CHANNEL_ID = os.getenv("DISCORD_WELCOME_CHANNEL_ID")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

matricola_counter = 1 
ANIME_BACKGROUND = "ANIME_BACKGROUND.png"
 

@bot.event
async def on_ready():
    print(f'✅ Bot connesso come {bot.user}')


@bot.event
async def on_member_join(member):
    global matricola_counter

    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).resize((100, 100))

    mask = Image.new("L", (100, 100), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 100, 100), fill=255)
    avatar = avatar.convert("RGBA")
    avatar.putalpha(mask)
    background = Image.open(ANIME_BACKGROUND).resize((400, 150))
    badge = background.copy()

    draw = ImageDraw.Draw(badge)
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(avatar)
    draw.text((120, 20),
              f"Benvenuto {member.name}",
              fill=(255, 255, 255),
              font=font)
    draw.text((120, 60),
              f"Matricola: {matricola_counter}",
              fill=(255, 255, 255),
              font=font)
    badgepath = f"badge_{member.id}.png"
    badge.paste(avatar, (10, 25), avatar)

    if not os.path.exists("imgBadge"):
        os.mkdir("imgBadge")
    
    badge.save(f"imgBadge/{badgepath}")

    print(badgepath)

    matricola_counter += 1

    channel = bot.get_channel(int(WELCOME_CHANNEL_ID))

    if isinstance(channel, discord.TextChannel):
        print(f"✅ Badge creato per {member.name}")
        await channel.send(f"🎉 Benvenuto {member.mention}!",
                           file=discord.File(badgepath))
    else:
        print(
            f"Errore: Il canale con ID {WELCOME_CHANNEL_ID} non è stato trovato o non è un canale di testo."
        )


if TOKEN:
    bot.run(TOKEN)
else:
    print("Token non trovato!")
