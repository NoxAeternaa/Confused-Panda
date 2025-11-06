import discord
from discord.ext import commands
import os

# -------- CONFIG --------
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1435035516855910510  # Channel-ID, wo die Nachricht gepostet werden soll
ROLE_IDS_TO_WATCH = [1429611742438228079]  # IDs der Rollen, auf die der Bot reagieren soll
GIF_URL = "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NjF0NXRwYjQxZnU1NnN3cXh5bngxM2N1ZXRkM2N4dHl4MHBydDd0biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/j6w4quCg3uzUSLFzZh/giphy.gif"
# -------------------------

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ist online: {bot.user}")

@bot.event
async def on_member_update(before, after):
    # Prüfen, ob eine neue Rolle hinzugekommen ist
    new_roles = [r for r in after.roles if r not in before.roles]
    for role in new_roles:
        if role.id in ROLE_IDS_TO_WATCH:
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                embed = discord.Embed()
                embed.set_image(url=GIF_URL)
                
                content = f"Huhu! Willkommen {after.mention} als **{role.name}**!\nFühl dich wie Zuhause! 🤗"
                await channel.send(content=content, embed=embed)

bot.run(TOKEN)
