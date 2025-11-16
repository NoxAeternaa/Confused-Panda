import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# -------- CONFIG --------
TOKEN = os.getenv("TOKEN")

# Öffentlicher Channel, in den alle Rollenänderungen kommen
public_promo_channel_id = 1439213467998359673

# Hier definierst du deine Rollen-Channel-Kombos
role_settings = {
    1435033624822026301: {  # Verlaufene Seele
        "channel_id":
        1435032765715316898,
        "message":
        " {usermention} ist eine **{rolename}**! Bitte helft ihr doch!",
        "gif_url":
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWtobDU3Y2lsbWhkMTh6cTdpNTU2dGtqZTczaDBlY2dhMmNoMHVqaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2GYYUGsLShvqRCWycQ/giphy.gif"
    },
    1435604655542374423: {  # Echo
        "channel_id":
        1435607533464326215,
        "message":
        "Upsi... {usermention} war wohl zu lange inaktiv und ist nun nur noch ein **{rolename}**.",
        "gif_url":
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDk4OHFmNjJnbDh6MDA0cHQwaHF6bDV1dWdkY3h0dHAwdmRqODgyMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zDmLzJfRkPkJ3Dw4b9/giphy.gif"
    },
    1233076320766787635: {  # Wanderer
        "channel_id":
        1435035039447646239,
        "message":
        "Ein **{rolename}** namens {usermention} besucht uns. Herzlich Willkommen!",
        "gif_url":
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmNlY2xrbnR3b2wzc2k5MGE4aDUxMGU5eGEwNWhkbWJqM3ZlZzA1cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/bZlcMvLxudr9VaTLXg/giphy.gif"
    },
    1429611841985839215: {  # Suchende Seele
        "channel_id":
        1435035111883014174,
        "message":
        "{usermention} will auch verrückt werden. Diese **{rolename}** muss sich erst noch erkunden.",
        "gif_url":
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZjZiNDFoeWI1YjB4ODVyOGp6enlhczN3YzJ2OWtycHl6bDYwMXhweCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/pPOR2prgwlCyOAlxgH/giphy.gif"
    },
    1233075847276269670: {  # Neue Seele
        "channel_id":
        1435035240069337088,
        "message":
        "{usermention} ist jetzt offiziell eine **{rolename}**! Willkommen und fühl dich wie Zuhause! 🤗!",
        "gif_url":
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3b3NqYzl5cW02ZjFmbzA1ODZpcWJjdDVrNWJxcWtlN2JtczN2ejB3dSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vG8S7ne4O60y2PT77g/giphy.gif"
    },
    1232802164364279832: {  # Erwachte Seele
        "channel_id":
        1435035439227469844,
        "message":
        "{usermention} ist endlich eine **{rolename}**! Du hast es geschafft",
        "gif_url":
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmZoaDhjdjV3dDd6eHQ5bGtrZnEwa2pjejk4bndxZXVvZXRqZjlpcyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/g9582DNuQppxC/giphy.gif"
    },
    1429611742438228079: {  # Bewahrte Seele
        "channel_id":
        1435035516855910510,
        "message":
        "Was machst du hier {usermention}? Eine **{rolename}** zu sein ist viel Verantwortung",
        "gif_url":
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2hpc3p3dDVwd3R2enV0b2s2ajFiYjF6OG16bXBnczVuM2VoeGJuYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/mMjzDtzFdnXaJhGyyx/giphy.gif"
    },
}
# -------------------------

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot ist online: {bot.user}")


@bot.event
async def on_member_update(before, after):
    # Prüfen, ob eine neue Rolle hinzugekommen ist
    new_roles = [r for r in after.roles if r not in before.roles]
    for role in new_roles:
        settings = role_settings.get(role.id)
        if settings:

            private_channel = bot.get_channel(settings["channel_id"])
            public_channel = bot.get_channel(public_promo_channel_id)

            # -------------------------
            # PRIVATE NACHRICHT
            # -------------------------
            private_msg = settings["message"].format(
                usermention=after.mention,
                rolename=role.name
            )

            embed_private = discord.Embed(
                description=private_msg,
                color=role.color
            )

            if settings.get("gif_url"):
                embed_private.set_image(url=settings["gif_url"])

            await private_channel.send(embed=embed_private)
            # -------------------------
            # ÖFFENTLICHER PROMO EMBED
            # -------------------------
            embed = discord.Embed(
                description=f"{after.mention} hat nun die Rolle **{role.name}**.",
                color=role.color  # ← AUTOMATISCHE Rollenfarbe
            )

            embed.set_author(name="Rollenänderung")

            await public_channel.send(embed=embed)


# -------- RUN --------
bot.run(TOKEN)