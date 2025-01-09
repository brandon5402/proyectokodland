import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

intents.message_content = True
FLASK_URL = 'http://127.0.0.1:5000/form_create'  # URL of your Flask app


@bot.event
async def on_ready():
    print(f'we have loggen in as {bot.user}')
    channel_id = 1312104693106868265
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("Bot is now online!")


@bot.command()
async def create_card(ctx, title: str, subtitle: str, text: str):
    if ctx.message.attachments:
        if len(ctx.message.attachments) > 1:
            await ctx.send("solo se puede subir una imagen")
            return
        else:
            img_data = requests.get(ctx.message.attachments[0].url).content
            img_filename = 'temp_image.png'
            with open(img_filename, 'wb') as handler:
                handler.write(img_data)

            files = {'img': open(img_filename, 'rb')}
            data = {'title': title, 'subtitle': subtitle, 'text': text}
            response = requests.post(FLASK_URL, files=files, data=data)

            if response.status_code == 200:
                await ctx.send('Card created successfully!')
            else:
                await ctx.send('Failed to create card.')

    else:
        await ctx.send("no se ha subido ninguna imagen")



bot.run("xd")
