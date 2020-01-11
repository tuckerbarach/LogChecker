import discord
import pandas as pd

# from selenium import webdriver
# from bs4 import BeautifulSoup
import filescrapping
client = discord.Client()
file = ""


@client.event
async def on_ready(self):
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Ready'))
    print('Logged on as {0}!'.format(self.user))


@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message("""Pfff, welcome loser {member.mention}""")


@client.event
async def on_message(message):
    global file
    id = client.get_guild(632412878565015555)
    channels = ["bot-commands"]
    valid_users = ["SwagRuler#0001", "SillyBoi#0001"]
    accepted_values = ['to', 'from', 'ign', 'autosell']
    ('Message from {0.author}: {0.content}'.format(message))

    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content == '-users':
            await message.channel.send(f"""Number of Members: {id.member_count}""")

        elif message.content == '-reboot':
            await message.channel.send("Rebooting now")
            client.destory()
            client.run("NjMyNDE0Nzc0MjczMjQ1MTk0.XaFFqQ.f8_eUDISEwlLplNzC-fgNbk7lQU")

        elif message.content == '-file':
            await message.channel.send("Please enter the full file directory for your log!")
            file = await client.wait_for('message')
            file = file.content
            if ".log" in file:
                await message.channel.send("File successfully selected!")
            else:
                await message.channel.send("Files must be in .log format!")

        elif message.content == '-getfile':
            await message.channel.send("The current file is: ``{}``".format(file))

        elif message.content == '-start':
            await message.channel.send("Type 'to', 'from', 'ign', or 'autosell' to begin")
            reply = await client.wait_for('message')

            if reply.content in accepted_values:
                print(reply)
                await message.channel.send("You picked: '{.content}'".format(reply))
                reply = reply.content
                if reply == 'to':
                    await message.channel.send(filescrapping.to_purchases(file, mode='r'))

            else:
                await message.channel.send("That is not an option, please try again!")


async def run_bot(message):
    await message.channel.send("You have selected: {message}")

client.run("NjMyNDE0Nzc0MjczMjQ1MTk0.XaFFqQ.f8_eUDISEwlLplNzC-fgNbk7lQU")
