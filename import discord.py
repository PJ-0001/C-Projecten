import discord
import base64
import asyncio

# Set your bot token here
TOKEN = 'MTEzODc2NTMxNzQ1NjI2OTM1OQ.GqgwPS.Og_r5JSDn0GOStOuessp-IPvt1vtnYdZcsDtyE'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.content.startswith('!req'):
        user_input = await get_user_input(message.author)
        encoded_message = base64.b64encode(user_input.encode("utf-8")).decode("utf-8")
        await send_embed_message(message.channel, user_input, encoded_message)

async def get_user_input(user):
    await user.send("Please enter the user ID of the suspect:")
    try:
        def check(msg):
            return msg.author == user
        user_input = await client.wait_for('message', check=check, timeout=60)
        return user_input.content.strip()
    except asyncio.TimeoutError:
        await user.send("You took too long to respond.")
        return None

async def send_embed_message(channel, user_input, encoded_message):
    embed = discord.Embed(
        title="Suspect User ID",
        description=f"ID: {user_input} - Token: {encoded_message}.",
        url="https://id.nerrix.ovh/",
        color=discord.Colour.red()
    )
    await channel.send(embed=embed)

client.run(TOKEN)
