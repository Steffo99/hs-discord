import re
import aiohttp
import discord

discord_token = ""
mashape_token = ""

d = discord.Client()

locale = "enUS"

def replace_html(string):
    string = string.replace("*", "\*")
    string = string.replace("_", " ")
    string = string.replace(r"\n", " ")
    string = string.replace("<b>", "**")
    string = string.replace("</b>", "**")
    string = string.replace("<i>", "_")
    string = string.replace("</i>", "_")
    return string

def create_embed(data):
    embed = discord.Embed(type="rich")
    embed.title = data["name"]
    embed.description = data["type"]
    embed.url = "http://media.services.zam.com/v1/media/byName/hs/cards/enus/" + data["cardId"] + ".png"
    embed.set_thumbnail(url=embed.url)
    if "rarity" in data:
        embed.add_field(name="Rarity", value=data["rarity"])
    if "cardSet" in data:
        embed.add_field(name="Expansion", value=data["cardSet"])
    if "playerClass" in data:
        embed.add_field(name="Class", value=data["playerClass"])
        if data["playerClass"] == "Druid":
            embed.colour = discord.Colour(85 * (255 ** 2) + 55 * 255 + 33)
        elif data["playerClass"] == "Hunter":
            embed.colour = discord.Colour(38 * (255 ** 2) + 92 * 255 + 33)
        elif data["playerClass"] == "Mage":
            embed.colour = discord.Colour(117 * (255 ** 2) + 128 * 255 + 169)
        elif data["playerClass"] == "Paladin":
            embed.colour = discord.Colour(203 * (255 ** 2) + 147 * 255 + 63)
        elif data["playerClass"] == "Priest":
            embed.colour = discord.Colour(224 * (255 ** 2) + 229 * 255 + 232)
        elif data["playerClass"] == "Rogue":
            embed.colour = discord.Colour(68 * (255 ** 2) + 62 * 255 + 68)
        elif data["playerClass"] == "Shaman":
            embed.colour = discord.Colour(44 * (255 ** 2) + 51 * 255 + 88)
        elif data["playerClass"] == "Warlock":
            embed.colour = discord.Colour(85 * (255 ** 2) + 55 * 255 + 93)
        elif data["playerClass"] == "Warrior":
            embed.colour = discord.Colour(118 * (255 ** 2) + 31 * 255 + 19)
    if "cost" in data:
        embed.add_field(name="Mana cost", value=str(data["cost"]) + " mana")
    if "attack" in data:
        embed.add_field(name="Attack", value=str(data["attack"]))
    if "health" in data:
        embed.add_field(name="Health", value=str(data["health"]))
    if "race" in data:
        embed.add_field(name="Tribe", value=data["race"])
    if "text" in data:
        embed.add_field(name="Text", value=replace_html(data["text"]), inline=False)
    if "flavor" in data:
        embed.set_footer(text=replace_html(data["flavor"]))
    return embed


@d.event
async def on_message(message: discord.Message):
    cards = re.findall("\[\[[^]]+]]", message.content)
    for card in cards:
        card = card.strip("[]")
        async with aiohttp.ClientSession() as session:
            headers = {
                'X-Mashape-Key': mashape_token,
                'Accept': 'application/json'
            }
            async with session.get(f"https://omgvamp-hearthstone-v1.p.mashape.com/cards/{card}", headers=headers) as r:
                data = await r.json()
                for obj in data:
                    if "collectible" in obj:
                        embed = create_embed(obj)
                        break
                else:
                    return
                await d.send_message(message.channel, embed=embed)


d.run(discord_token)