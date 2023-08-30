import asyncio
import os
import discord
import zipfile
import urllib
import filescrapping
import leaderboardsheet
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import sqlite3
from sqlite3 import Error
import MySQLdb
from io import BytesIO
import get_messages
import threading
import time
import datasheet

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

user_info = [] # array storing player's info
contents = ""
commands = ["-start", "-file", "-filter", "-getfile", "-merge", "-paste", "-preview", "-reload", "-swap", "-time", "-type", "-debug", "-redo", "-track", "-ifilter"]
the_channel_id = None
log_type = ""
file_url = ""
past_url = ""

BOT_IMAGE = "IMAGE.png"
COLOR = discord.Colour.blue()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}



users = {
 
}

functions = {
    "ign_transactions": "Transaction Logs",
    "auto_sell": "Auto Sell Logs",
    "trade_logs": "Trade Logs",
    "withdrawals": "Withdrawal Logs",
    "deposits": "Deposit Logs",
    "mobcoin_balance": "Mobcoin Logs",
    "chat_logs": "Chat Logs",
    "island_chat": "Island Chat Logs",
    "gather_messages": "Message Logs",
    "pay_logs": "Pay Logs",
    "vault_logs": "Vault Logs",
    "auction_logs": "Auction Logs",
    "drop_logs": "Drop Logs",
    "void_chest": "Voidchest Logs",
    "ftop_logs": "FTop Logs",
    "land_logs": "Land Logs",
    "spawner_chunk_logs": "Spawner Chunk Logs",
    "raid_updates": "Raid Update Logs",
    "faction_lockdowns": "Lockdown Logs",
    "coinflip": "Coinflip Logs",
    "rps": "RPS Logs",
    "cegg_logs": "CEGG Logs",
    "balance_logs": "Balance Logs",
    "tpa_logs": "TPA Logs",
    "crate_logs": "Crate Logs",
    "chunkhopper_logs": "ChunkHopper Logs",
    "from_purchases": "From Shop Logs",
    "to_purchases": "To Shop Logs",
    "filter_file": "Filter"

}

class BotUser:
    def __init__(self, name, file, channel_id, user_contents, gamemode, user_id, current_function, current_params):
        self.name = name
        self.file_name = file
        self.channel_id = channel_id
        self.user_contents = user_contents
        self.gamemode = gamemode
        self.user_id = user_id
        self.current_function = current_function
        self.current_params = current_params

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "random":
            await client.get_channel(632412878565015559).send(f"""Welcome {member.mention}!""")

@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "random":
            await client.get_channel(632412878565015559).send(f"""{member.display_name} has left... :(""")

@client.event
async def on_message(message, self=None):
    global contents, user_info, log_type, file_url
    current_gamemode = "None right now"
    current_contents = "not selected"
    current_user = "user"
    obj_ref = None

    user_already_in = False

    for user in user_info:
        if message.author.name in user.name:
            user_already_in = True
            current_gamemode = user.gamemode
            current_contents = user.user_contents
            current_user = user.name
            obj_ref = user
            break


    if str(message.author) == "LogChecker#0238" and len(message.attachments) > 0:
        file_url = message.jump_url

    if message.content.startswith("https://s3.company.com") and user_already_in:
        # if true: add user to 2D array and carry out functions done
        print("reach")
        await client.get_channel(message.channel.id).send("Loading... This may take a few seconds...")

        obj_ref.file = message.content # updates file
        obj_ref.user_contents = zip_contents(obj_ref.file)
        gm = obj_ref.user_contents[0:50] # for later use

        obj_ref.gamemode = "Skyblock" if "origins" in gm or "genesis" in gm \
            or "chaos" in gm or "chicken" in gm or "creeper" in gm \
            or "pig" in gm or "pmc2_sb" in gm or "space" in gm \
            or "western" in gm else "Factions" if "amber" in gm \
            or "onyx" in gm or "ruby" in gm \
            else "Prison" if "prison" in gm or "blaze" in gm or "pmc2_prison" in gm \
            else "Outlands" if "outlands" in gm else "Robbery"

        # Updating complete:
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name=(obj_ref.gamemode + " log successfully selected!"),
                         icon_url=BOT_IMAGE)
        embed.add_field(name="File selected from start to end", value="Update times with -time",
                        inline=False)
        await client.get_channel(message.channel.id).send(embed=embed)

    elif message.content.startswith("https://s3.company.com") and not user_already_in:
        await client.get_channel(message.channel.id).send("Loading... This may take a few seconds...")

        user_contents = zip_contents(message.content)
        gm = user_contents[0:50]
        print(gm)
        gamemode = "Skyblock" if "origins" in gm or "genesis" in gm \
            or "chaos" in gm or "chicken" in gm or "creeper" in gm \
            or "pig" in gm or "pmc2_sb" in gm or "space" in gm \
            or "western" in gm else "Factions" if "amber" in gm \
            or "onyx" in gm or "ruby" in gm \
            else "Prison" if "azkaban" in gm or "blaze" in gm or "pmc2_prison" in gm \
            else "Outlands" if "outlands" in gm else "Robbery"

        user_info.append(BotUser(message.author.name, message.content, message.channel.id, user_contents, gamemode, message.author.id, None, []))

        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name=(gamemode + " log successfully selected!"),
                         icon_url=BOT_IMAGE)
        embed.add_field(name="File selected from start to end", value="Update times with -time",
                        inline=False)
        await client.get_channel(message.channel.id).send(embed=embed)

    elif message.content in commands and user_already_in:
        log_type = current_gamemode
        await run_command(message.content, message.channel.id, current_gamemode, current_contents, current_user, message.author.id, message.author) # runs command

    elif message.content in commands:
        await client.get_channel(message.channel.id).send("No file selected! Paste your https://s3.company.com link here first!")

    elif "-score" in message.content:
        name = ""
        if message.content == '-score':
            author = message.author.name
            name = list(users.keys())[list(users.values()).index(message.author.id)]  # gets the nickname

        else:
            name = message.content.replace("-score ", "")
            name = name.capitalize()
        try:
            await client.get_channel(message.channel.id).send(name + "'s score is: " + str(get_score(name)))

        except Exception as e:
            print("This is the error: " + str(e))
            try:
                if name == "J4n8":
                    await client.get_channel(message.channel.id).send("J4N8's score is: " + str(leaderboardsheet.get_player_score("J4N8")))
                elif name == "Imnear":
                    await client.get_channel(message.channel.id).send("ImNear's score is: " + str(leaderboardsheet.get_player_score("ImNear")))
                elif name == "Xmc":
                    await client.get_channel(message.channel.id).send("xMc's score is: " + str(leaderboardsheet.get_player_score("xMc")))
                else:
                    await client.get_channel(message.channel.id).send("That user is not found!")

            except Exception as e:
                await client.get_channel(message.channel.id).send("That user is not found!")

    elif message.content == '-users':
        await client.get_channel(message.channel.id).send(f"""Number of Members: {client.get_guild(632412878565015555).member_count}""")

    elif message.author.name != "LogChecker" and message.content[0] == '-' and not any(char.isdigit() for char in message.content):  # incase people are chatting, don't get spammed
        await client.get_channel(message.channel.id).send("Not a command! Check <#645483940890542080>")

async def reset_user(user_name):
    pass
    # global user_info
    # index = 0
    # for member in user_info:
    #     if member.name == user_name:
    #         user_info.pop(index)
    #         print("Cleared info for " + user_name + " at index: " + str(index))
    #         break
    #     else:
    #         index += 1

def check(message):
    print("Check: " + message.content + " " + str(message.author))
    return message.content != "" and str(message.author) != "LogChecker#0238" and "s3.company.com" not in message.content


def set_function(user_id, function_name):
    index = 0
    for user in user_info:
        if user.user_id == user_id:
            user.current_function = "filescrapping." + function_name
            return user
        index += 1


async def run_command(command, channel_id, log_type, contents, user, user_id, member_obj):
    global the_channel_id
    the_channel_id = channel_id
    channel = client.get_channel(channel_id)

    servers = client.guilds
    roles = member_obj.roles

    if command == '-filter':
        await channel.send("Please enter what you want each line to contain:\n\n"
        "If you want all lines to contain multiple phrases, separate each item with an ampersand (&).\n"
        "If you want all lines to contain at least one of multiple phrases, separate each item with a vertical line (|).")

        filter = (await client.wait_for('message', check=check)).content
        await channel.send("Commencing...")
        is_all = not filter.find("|") != -1 # determines if the search is in "OR" mode or not
        filtered_file = filescrapping.filter_file(contents, filter.lower(), is_all, True)
        await channel.send(file=filtered_file)
        await post_log(roles, [member_obj.display_name + ' completed a filter for "' + filter + '"'])

        info = set_function(user_id, "filter_file")
        info.current_params = [filter.lower(), is_all]
        update_score(member_obj.display_name)  # Updates scoreboard if -filter sequence completed

    elif command == '-ifilter':
        await channel.send("Please enter a filter for lines to be removed:\n\n"
                           "If you want all lines to not contain multiple phrases, separate each item with an ampersand (&).\n"
                           "If you want all lines to not contain at least one of multiple phrases, separate each item with a vertical line (|).")

        filter = (await client.wait_for('message', check=check)).content
        await channel.send("Commencing...")
        is_all = not filter.find("|") != -1  # determines if the search is in "OR" mode or not
        filtered_file = filescrapping.filter_file(contents, filter.lower(), is_all, False)
        await channel.send(file=filtered_file)
        await post_log(roles, [member_obj.display_name + ' completed an inverse filter for "' + filter + '"'])

        info = set_function(user_id, "filter_file")
        info.current_params = [filter.lower(), is_all]
        update_score(member_obj.display_name)  # Updates scoreboard if -filter sequence completed

    elif command == '-reload':
        file = "None selected! Upload a .zip, .txt, or .log file!"
        contents = ""
        file_contents = ["Backup Contents"]
        file_names = ["Backup"]
        file_gamemode = ["None"]
        is_first_file = True
        log_type = ""
        await channel.send("Successfully reloaded!")


    elif command == '-track':
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Track Down Items!",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Spawner Tracker", value="1",
                        inline=False)
        await channel.send(embed=embed)

        reply = (await client.wait_for('message', check=check)).content

        if reply == '1':
            # Spawner Tracker:
            await channel.send("Copy & Paste the exact dropped line (Ex: wvrst dropped {MOB_SPAWNER:0 x22 | §eCreeper §fSpawner | null} at clay_flat x2473 y200 z2456)")
            start_line = (await client.wait_for('message', check=check)).content

            await channel.send("Commencing...")
            results_file = filescrapping.spawner_tracker(contents, start_line)

            embed = discord.Embed(
                colour=COLOR
            )

            embed.set_author(name="Spawner Tracker Results:",
                             icon_url=BOT_IMAGE)
            await channel.send(embed=embed)
            await channel.send(file=results_file)

            await post_log(roles, [user + " completed Spawner Tracker", results_file])


    elif command == '-redo':
        await channel.send("Commencing...")
        index = 0
        files = []
        display_results = []
        current_user = None
        for user in user_info:
            if user.user_id == user_id:
                results = eval(user.current_function)(contents, *user.current_params)
                current_user = user
            index += 1

        if user.current_function != "filescrapping.filter_file":
            for obj in results:
                if isinstance(obj, discord.file.File):
                    files.append(obj)

                else:
                    display_results.append(obj)

            embed = discord.Embed(
                colour=COLOR
            )
            embed.set_author(name=(functions[current_user.current_function.replace("filescrapping.", "")] + " Redo"),
                             icon_url=BOT_IMAGE)
            embed.add_field(name="Results:", value=str(str(display_results).strip('[]')),
                            inline=False)
            await channel.send(embed=embed)

            if len(files) > 0:
                for file in files:
                    await channel.send(file=file)

        else:
            await channel.send(file=results)

        print("'" + current_user.current_function.replace("filescrapping.", "") + "'")
        await post_log(roles, [member_obj.display_name + " completed " + functions[current_user.current_function.replace("filescrapping.", "")] + " Redo"])



    elif command == '-debug':
        pass
        #if str(message.author) == "SwagRuler#0001" or str(message.author) == "B3n#0001":
            #await channel.send(file_names)
            #await channel.send(file)
            #await channel.send(file_gamemode)
            #await channel.send(log_type)
            #await channel.send(contents[0:500])
            #await channel.send("Author: " + str(message.author))
            #await channel.send("Current User: " + str(current_user))
            #await channel.send("Time Left: " + str(time_left))

    elif command == '-preview':
        await channel.send("Preview Loading...")

        txt_file = open("Preview.txt", "w+")
        if len(contents) > 10000:
            txt_file.write(contents[0:10000])
        else:
            txt_file.write(contents)
        txt_file.close()
        txt_file = open("Preview.txt", "r")  # updates file's contents

        txt_file = discord.File(txt_file)
        txt_file.close()
        await channel.send(file=txt_file)


    elif command == '-paste':
        if len(contents) < 5000000:  # 5 million bytes is 5MB
            await channel.send("Commencing...")
            paste_file = open("Paste File.txt", "w+")
            paste_file.write(contents)
            paste_file.close()
            paste_file = open("Paste File.txt", "r")
            paste_file = discord.File(paste_file)
            paste_file.close()
            await channel.send(file=paste_file)
        else:
            await channel.send("The current selection is greater than 5MB. Please -filter is more!")

    elif command == '-start':
        author = list(users.keys())[list(users.values()).index(user_id)]  # gets the nickname
        user = author
        await channel.send(embed=list_start(log_type))

        reply = (await client.wait_for('message', check=check)).content
        # starts the 10 minute countdown
        await asyncio.wait_for(reset_user(user), timeout=600)

        if log_type == "Factions":
            if reply == '1':
                await selling_trans(log_type, contents, roles, user, set_function(user_id, "ign_transactions"))

            elif reply == '2':
                await auto_sell_bot(contents, roles, user, set_function(user_id, "auto_sell"))

            elif reply == '3':
                await withdrawals(contents, roles, user, set_function(user_id, "withdrawals"))

            elif reply == '4':
                await deposits(contents, roles, user, set_function(user_id, "deposits"))

            elif reply == '5':
                await mobcoins(contents, roles, user, set_function(user_id, "mobcoin_balance"))

            elif reply == '6':
                await chat_logs(contents, roles, user, set_function(user_id, "chat_logs"))

            elif reply == '7':
                await messages(contents, roles, user, set_function(user_id, "gather_messages"))

            elif reply == '8':
                await pay(contents, roles, user, set_function(user_id, "pay_logs"))

            elif reply == '9':
                await trading(contents, roles, user, set_function(user_id, "trade_logs"))

            elif reply == '10':
                await auction(contents, roles, user, set_function(user_id, "auction_logs"))

            elif reply == '11':
                await voidchest(contents, roles, user, set_function(user_id, "void_chest"))

            elif reply == '12':
                await drops(contents, roles, user, set_function(user_id, "drop_logs"))

            elif reply == '13':
                await ftop(contents, roles, user, set_function(user_id, "ftop_logs"))

            elif reply == '14':
                await land(contents, roles, user, set_function(user_id, "land_logs"))

            elif reply == '15':
                await spawner_chunk(contents, roles, user, set_function(user_id, "spawner_chunk_logs"))

            elif reply == '16':
                await updates(contents, roles, user, set_function(user_id, "raid_updates"))

            elif reply == '17':
                await lockdowns(contents, roles, user, set_function(user_id, "faction_lockdowns"))

            elif reply == '18':
                await coinflip(contents, roles, user, set_function(user_id, "coinflip"))

            elif reply == '19':
                await rps(contents, roles, user, set_function(user_id, "rps"))

            elif reply == '20':
                await cegg(contents, roles, user, set_function(user_id, "cegg_logs"))

            elif reply == '21':
                await balance(contents, roles, user, set_function(user_id, "balance_logs"))

            elif reply == '22':
                await tpa(contents, roles, user, set_function(user_id, "tpa_logs"))

            elif reply == '23':
                await crates(contents, roles, user, set_function(user_id, "crate_logs"))

        elif log_type == "Skyblock":
            if reply == '1':
                await to_shop_bot(contents, roles, user, set_function(user_id, "to_purchases"))

            elif reply == '2':
                await from_shop_bot(contents, roles, user, set_function(user_id, "from_purchases"))

            elif reply == '3':
                await selling_trans(log_type, contents, roles, user, set_function(user_id, "ign_transactions"))

            elif reply == '4':
                await auto_sell_bot(contents, roles, user, set_function(user_id, "auto_sell"))

            elif reply == '5':
                await withdrawals(contents, roles, user, set_function(user_id, "withdrawals"))

            elif reply == '6':
                await deposits(contents, roles, user, set_function(user_id, "deposits"))

            elif reply == '7':
                await mobcoins(contents, roles, user, set_function(user_id, "mobcoin_balance"))

            elif reply == '8':
                await chat_logs(contents, roles, user, set_function(user_id, "chat_logs"))

            elif reply == '9':
                await island_chat_messages(contents, roles, user, set_function(user_id, "island_chat"))

            elif reply == '10':
                await messages(contents, roles, user, set_function(user_id, "gather_messages"))

            elif reply == '11':
                await pay(contents, roles, user, set_function(user_id, "pay_logs"))

            elif reply == '12':
                await trading(contents, roles, user, set_function(user_id, "trade_logs"))

            elif reply == '13':
                await vault(contents, roles, user, set_function(user_id, "vault_logs"))

            elif reply == '14':
                await auction(contents, roles, user, set_function(user_id, "auction_logs"))

            elif reply == '15':
                await coinflip(contents, roles, user, set_function(user_id, "coinflip"))

            elif reply == '16':
                await rps(contents, roles, user, set_function(user_id, "rps"))

            elif reply == '17':
                await balance(contents, roles, user, set_function(user_id, "balance_logs"))

            elif reply == '18':
                await drops(contents, roles, user, set_function(user_id, "drop_logs"))

            elif reply == '19':
                await tpa(contents, roles, user, set_function(user_id, "tpa_logs"))

            elif reply == '20':
                await crates(contents, roles, user, set_function(user_id, "crate_logs"))

            elif reply == '21':
                await chunkhopper(contents, roles, user, set_function(user_id, "chunkhopper_logs"))

        elif log_type == "Prison":
            if reply == '1':
                await selling_trans(log_type, contents, roles, user, set_function(user_id, "ign_transactions"))

            elif reply == '2':
                await withdrawals(contents, roles, user, set_function(user_id, "withdrawals"))

            elif reply == '3':
                await deposits(contents, roles, user, set_function(user_id, "deposits"))

            elif reply == '4':
                await vault(contents, roles, user, set_function(user_id, "vault_logs"))

            elif reply == '5':
                await chat_logs(contents, roles, user, set_function(user_id, "chat_logs"))

            elif reply == '6':
                await island_chat_messages(contents, roles, user, set_function(user_id, "island_chat"))

            elif reply == '7':
                await messages(contents, roles, user, set_function(user_id, "gather_messages"))

            elif reply == '8':
                await pay(contents, roles, user, set_function(user_id, "pay_logs"))

            elif reply == '9':
                await trading(contents, roles, user, set_function(user_id, "trade_logs"))

            elif reply == '10':
                await auction(contents, roles, user, set_function(user_id, "auction_logs"))

            elif reply == '11':
                await coinflip(contents, roles, user, set_function(user_id, "coinflip"))

            elif reply == '12':
                await rps(contents, roles, user, set_function(user_id, "rps"))

            elif reply == '13':
                await balance(contents, roles, user, set_function(user_id, "balance_logs"))

            elif reply == '14':
                await drops(contents, roles, user, set_function(user_id, "drop_logs"))

            elif reply == '15':
                await tpa(contents, roles, user, set_function(user_id, "tpa_logs"))

            elif reply == '16':
                await crates(contents, roles, user, set_function(user_id, "crate_logs"))

        elif log_type == "Outlands":
            if reply == '1':
                await messages(contents, roles, user, set_function(user_id, "gather_messages"))

            elif reply == '2':
                await chat_logs(contents, roles, user, set_function(user_id, "chat_logs"))

            elif reply == '3':
                await tpa(contents, roles, user, set_function(user_id, "tpa_logs"))

            elif reply == '4':
                await crates(contents, roles, user, set_function(user_id, "crate_logs"))

        elif log_type == "Robbery":
            if reply == '1':
                await trading(contents, roles, user, set_function(user_id, "trade_logs"))

            elif reply == '2':
                await withdrawals(contents, roles, user, set_function(user_id, "withdrawals"))

            elif reply == '3':
                await deposits(contents, roles, user, set_function(user_id, "deposits"))

            elif reply == '4':
                await chat_logs(contents, roles, user, set_function(user_id, "chat_logs"))

            elif reply == '5':
                await messages(contents, roles, user, set_function(user_id, "gather_messages"))

            elif reply == '6':
                await drops(contents, roles, user, set_function(user_id, "drop_logs"))

            elif reply == '7':
                await coinflip(contents, roles, user, set_function(user_id, "coinflip"))

            elif reply == '8':
                await rps(contents, roles, user, set_function(user_id, "rps"))

            elif reply == '9':
                await tpa(contents, roles, user, set_function(user_id, "tpa_logs"))

            elif reply == '10':
                await balance(contents, roles, user, set_function(user_id, "balance_logs"))

            elif reply == '11':
                await crates(contents, roles, user, set_function(user_id, "crate_logs"))


        # If improper -start selection:
        else:
            embed = discord.Embed(
                colour=COLOR
            )

            embed.set_author(name="That is not an option, please try again!",
                             icon_url=BOT_IMAGE)
            await channel.send(embed=embed)

        # user = ""
        # if str(author.display_name) == "":
        #     user = str(author.name)
        # else:
        #     user = str(author.display_name)
        update_score(user) # Updates scoreboard if -start sequence completed

    elif command == '-time':
        await channel.send("Please enter the starting time (Ex: 04:00:23 or 13:32:59)")
        start_time = (await client.wait_for('message', check=check)).content
        if "[" + start_time + "]" in contents:
            await channel.send("Please enter the ending time (Ex: 23:59:59)")
            end_time = (await client.wait_for('message', check=check)).content
            if "[" + end_time + "]" in contents:
                # Code change contents to just the contents of selected times:

                is_line_within_times = False
                lines = contents.split("\n")
                time_file = open("time_contents.txt", "w+")
                for line in lines:
                    if not is_line_within_times:
                        if line[1:9] == start_time:
                            is_line_within_times = True
                    else:
                        if line[1:9] == end_time:
                            break
                        else:
                            time_file.write(line + "\n")

                time_file.close()
                time_file = open("time_contents.txt", "r")
                for obj in user_info:
                    if obj.name == user:
                        obj.current_contents = time_file.read()
                time_file.close()
                await channel.send("Time contents successfully selected!")
            else:
                await channel.send("Invalid end time or that end time is not in this file. Try again with -time!")
        else:
            await channel.send("Invalid start time or that start time is not in this file. Try again with -time!")

# elif message.content[0] == '-' and not any(char.isdigit() for char in message.content): # incase people are chatting, don't get spammed
#     await channel.send("Not a command! Check <#645483940890542080>")




async def to_shop_bot(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    await channel.send("Commencing...")
    sell_all_counter, shop_counter, ores_shop_counter, vip_shop, drops_shop, food_shop, \
    redstone_shop, blocks_shop, farming_shop, dyes_shop, total \
        = filescrapping.to_purchases(contents)
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Amounts Sold To The Shop",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Sell All Counter:", value=sell_all_counter, inline=False)
    embed.add_field(name="/Shop Counter:", value=shop_counter, inline=False)
    embed.add_field(name="Ores Shop Counter:", value=ores_shop_counter, inline=False)
    embed.add_field(name="VIP Shop Counter:", value=vip_shop, inline=False)
    embed.add_field(name="Drops Shop Counter:", value=drops_shop, inline=False)
    embed.add_field(name="Food Shop Counter:", value=food_shop, inline=False)
    embed.add_field(name="Redstone Shop Counter:", value=redstone_shop, inline=False)
    embed.add_field(name="Blocks Shop Counter", value=blocks_shop, inline=False)
    embed.add_field(name="Farming Shop Counter:", value=farming_shop, inline=False)
    embed.add_field(name="Dyes Counter:", value=dyes_shop, inline=False)
    embed.add_field(name="Total:", value=total, inline=False)

    await channel.send(embed=embed)

    info.current_params = []

    await post_log(roles, [user + " completed To Shop Logs"])


async def from_shop_bot(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    await channel.send("Commencing...")
    ores_shop_counter, redstone_shop, vip_shop, drops_shop, farming_shop, \
    food_shop, blocks_shop, colored_blocks, combat_shop, dyes_shop, potions_shop, total \
        = filescrapping.from_purchases(contents)
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Amounts Bought From The Shop",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Ores Shop Counter:", value=ores_shop_counter, inline=False)
    embed.add_field(name="Redstone Shop Counter:", value=redstone_shop, inline=False)
    embed.add_field(name="VIP Shop Counter:", value=vip_shop, inline=False)
    embed.add_field(name="Drops Shop Counter:", value=drops_shop, inline=False)
    embed.add_field(name="Farming Shop Counter:", value=farming_shop, inline=False)
    embed.add_field(name="Food Shop Counter:", value=food_shop, inline=False)
    embed.add_field(name="Blocks Shop Counter:", value=blocks_shop, inline=False)
    embed.add_field(name="Colored Blocks Shop Counter:", value=colored_blocks, inline=False)
    embed.add_field(name="Combat Shop Counter:", value=combat_shop, inline=False)
    embed.add_field(name="Dyes Shop Counter:", value=dyes_shop, inline=False)
    embed.add_field(name="Potions Counter:", value=potions_shop, inline=False)
    embed.add_field(name="Total:", value=total, inline=False)
    await channel.send(embed=embed)

    info.current_params = []

    await post_log(roles, [user + " completed From Shop Logs"])

async def selling_trans(log_type, contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    await channel.send("Please enter the IGN you want to lookup")
    username = (await client.wait_for('message', check=check)).content
    await channel.send("Commencing...")

    if log_type == "Skyblock":
        to_shop, sell_chest = filescrapping.ign_transactions(contents, username, log_type)
    else:
        to_shop = filescrapping.ign_transactions(contents, username, log_type)

    info.current_params = [username, log_type]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="IGN Transactions",
                     icon_url=BOT_IMAGE)
    embed.add_field(name=("Amount " + username + " Sold To /Shop:"),
                    value=("$" + to_shop), inline=False)

    if log_type == "Skyblock":
        embed.add_field(name=("Amount " + username + " Earned From SellChests:"),
                        value=("$" + sell_chest), inline=False)
    await channel.send(embed=embed)

    await post_log(roles, [user + " completed Selling Transaction Logs"])


async def auto_sell_bot(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    await channel.send("Do you want to flag auto-sellers? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Flag mode commencing...")
        auto_sellers = filescrapping.flag_autoseller(contents)
        auto_sellers = auto_sellers.split("!")

        try:
            for i in range(len(auto_sellers)):
                embed = discord.Embed(
                    colour=COLOR
                )

                embed.add_field(value=auto_sellers[i], inline=False)
                await channel.send(embed=embed)

            await channel.send("Flag mode done!")
        except:
            embed = discord.Embed(
                colour=COLOR
            )

            embed.set_author(name="Nobody was flagged for auto-selling!",
                             icon_url=BOT_IMAGE)
            await channel.send(embed=embed)

    else:
        await channel.send("Please send the IGN you want to lookup")
        username = (await client.wait_for('message', check=check)).content

        info.current_params = info.current_params.append(username)

        if username != "":

            info.current_params = [username]

            await channel.send("Commencing...")
            embed = discord.Embed(
                colour=COLOR
            )

            embed.set_author(name=(username + "'s Selling Stats"),
                             icon_url=BOT_IMAGE)
            embed.add_field(name="Results:", value=filescrapping.auto_sell(contents, username),
                            inline=False)
            await channel.send(embed=embed)

        else:
            await channel.send("An error has occurred, please try again!")


async def withdrawals(contents, roles, user, info):
    username = ""
    channel = client.get_channel(the_channel_id)
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Money Withdrawals:", value="1", inline=False)
    embed.add_field(name="EXP Withdrawals:", value="2", inline=False)
    if log_type == "Prison":
        embed.add_field(name="Token Withdrawals:", value="3", inline=False)
    await channel.send(embed=embed)
    type = (await client.wait_for('message', check=check)).content

    if type == '1':
        type = "money"
    elif type == '2':
        type = "exp"
    elif log_type == "Prison" and type == '3':
        type = "tokens"

    await channel.send("Do you want to search for a specific user? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please send the IGN you want to lookup")
        username = (await client.wait_for('message', check=check)).content
        await channel.send("Commencing...")
        results_file, total = filescrapping.withdrawals(contents, type, log_type, username)

    else:
        await channel.send("Commencing....")
        results_file, total = filescrapping.withdrawals(contents, type, log_type, username)

    info.current_params = [type, log_type, username]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Withdrawals",
                     icon_url=BOT_IMAGE)
    if type == 'money':
        embed.add_field(name="Total Money Withdrawn:", value=str(total), inline=False)
    elif type == 'exp':
        embed.add_field(name="Total EXP Withdrawn:", value=str(total), inline=False)
    elif type == 'tokens':
        embed.add_field(name="Total Tokens Withdrawn:", value=str(total), inline=False)

    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Withdraw Logs", results_file])


async def deposits(contents, roles, user, info):
    username = ""
    channel = client.get_channel(the_channel_id)
    results_file = ""
    total = 0
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Money Deposits:", value="1", inline=False)
    embed.add_field(name="EXP Deposits:", value="2", inline=False)
    if log_type == "Prison":
        embed.add_field(name="Token Deposits:", value="3", inline=False)
    await channel.send(embed=embed)
    type = (await client.wait_for('message', check=check)).content

    if type == '1':
        type = "money"
    elif type == '2':
        type = "exp"
    elif log_type == "Prison" and type == '3':
        type = "tokens"

    await channel.send("Do you want to search for a specific user? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please send the IGN you want to lookup")
        username = (await client.wait_for('message', check=check)).content
        await channel.send("Commencing...")
        results_file = filescrapping.deposits(contents, type, log_type, username)

    else:
        await channel.send("Commencing....")
        results_file, total = filescrapping.deposits(contents, type, log_type, username)

    info.current_params = [type, log_type, username]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Deposits",
                     icon_url=BOT_IMAGE)
    if type == 'money':
        embed.add_field(name="Total Money Deposited:", value=str(total), inline=False)
    elif type == 'exp':
        embed.add_field(name="Total EXP Deposited:", value=str(total), inline=False)
    elif type == 'tokens':
        embed.add_field(name="Total Tokens Deposited:", value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Deposit Logs", results_file])


async def mobcoins(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    await channel.send("Please send the IGN you want to lookup")
    username = (await client.wait_for('message', check=check)).content
    await channel.send("Commencing...")

    results_file = filescrapping.mobcoin_balance(contents, username)

    info.current_params = [username]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=("MobCoin Balances of " + username),
                     icon_url=BOT_IMAGE)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed MobCoin Logs", results_file])


async def chat_logs(contents, roles, user, info):
    total = 0
    results_file = ""
    username = ""
    keyword = ""
    channel = client.get_channel(the_channel_id)
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Search By Keyword:", value="1", inline=False)
    embed.add_field(name="Search By Username:", value="2", inline=False)
    embed.add_field(name="Search By Keyword And Username:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Keyword"
        await channel.send("Please enter the word that you are interested in")
        keyword = (await client.wait_for('message', check=check)).content
    elif mode == '2':
        mode = "Username"
        await channel.send("Please enter the IGN that you are interested in")
        username = (await client.wait_for('message', check=check)).content
    elif mode == '3':
        mode = "Both"
        await channel.send("Please enter the word that you are interested in")
        keyword = (await client.wait_for('message', check=check)).content
        await channel.send("Please enter the IGN that you are interested in")
        username = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.chat_logs(contents, mode, keyword, username, log_type)

    info.current_params = [mode, keyword, username, log_type]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Chat Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Messages Captured In " + str(mode) + " Mode:",
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Chat Logs and found " + str(total) + " results", results_file])


async def island_chat_messages(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    await channel.send("What are the island coordinates that you are looking for? (Ex: -49/5)")
    coords = (await client.wait_for('message', check=check)).content
    await channel.send("Commencing...")
    results_file = filescrapping.island_chat(contents, coords)

    info.current_params = [coords]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(coords + "'s Island Chat"),
                     icon_url=BOT_IMAGE)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Island Chat Logs", results_file])


async def messages(contents, roles, user, info):
    user2 = ""
    channel = client.get_channel(the_channel_id)
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Do you want to read the conversation between two players?",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Read All Messages From Player", value="1", inline=False)
    embed.add_field(name="Read Two Player Conversation", value="2", inline=False)
    await channel.send(embed=embed)

    type = (await client.wait_for('message', check=check)).content

    if type == '1':
        await channel.send("Please enter the IGN that you want to view messages of")
        user1 = (await client.wait_for('message', check=check)).content
    else:
        await channel.send("Please enter one of the two player's IGN now")
        user1 = (await client.wait_for('message', check=check)).content
        await channel.send("Please enter the other IGN now")
        user2 = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.gather_messages(contents, user1, user2)

    info.current_params = [user1, user2]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Messages",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Total Messages Found:", value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Messages Logs and found " + str(total) + " results", results_file])


async def pay(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    sender = ""
    receiver = ""
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Payments From Sender to Receiver:", value="1", inline=False)
    embed.add_field(name="Payments From Sender:", value="2", inline=False)
    embed.add_field(name="Payments to Receiver:", value="3", inline=False)
    embed.add_field(name="All Payments:", value="4", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Both"
        await channel.send("Please enter the IGN that sent the payments")
        sender = (await client.wait_for('message', check=check)).content
        await channel.send("Please enter the IGN that received the payments")
        receiver = (await client.wait_for('message', check=check)).content

    elif mode == '2':
        mode = "Send Only"
        await channel.send("Please enter the IGN that sent the payments")
        sender = (await client.wait_for('message', check=check)).content

    elif mode == '3':
        mode = "Receive Only"
        await channel.send("Please enter the IGN that received the payments")
        receiver = (await client.wait_for('message', check=check)).content

    else:
        mode = "All"
    await channel.send("Commencing...")


    results_file, amount, count = filescrapping.pay_logs(contents, sender, receiver, mode)

    info.current_params = [sender, receiver, mode]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Payments"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Money Transferred In " + str(mode) + " Mode:",
                    value=("$" + str(amount)), inline=False)
    embed.add_field(name="/Pay Count:", value=str(count), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Pay Logs and found " + str(count) + " results\nMoney Transferred In " + str(mode) + " Mode: $" + str(amount), results_file])


async def trading(contents, roles, user, info):
    sender = ""
    receiver = ""
    channel = client.get_channel(the_channel_id)
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Trades From Sender to Receiver:", value="1", inline=False)
    embed.add_field(name="Trades To Receiver or From Sender:", value="2", inline=False)
    embed.add_field(name="All Trades:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Both"
        await channel.send("Please enter the IGN that sent the trade")
        sender = (await client.wait_for('message', check=check)).content
        await channel.send("Please enter the IGN that received the trade")
        receiver = (await client.wait_for('message', check=check)).content
    elif mode == '2':
        mode = "Send/Receive"
        await channel.send("Please enter the IGN that sent or received the trade")
        sender = (await client.wait_for('message', check=check)).content
    else:
        mode = "All"

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select What To Search For:",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Everything:", value="1", inline=False)
    embed.add_field(name="Mob Spawners:", value="2", inline=False)
    if log_type == "Skyblock":
        embed.add_field(name="Mobcoin Trophies", value="3", inline=False)
        embed.add_field(name="Sell Chests", value="4", inline=False)
        embed.add_field(name="Robots", value="5", inline=False)
        embed.add_field(name="Infinity Chests", value="6", inline=False)
    elif log_type == "Prison":
        embed.add_field(name="Robots", value="3", inline=False)
        embed.add_field(name="Pickaxes", value="4", inline=False)
    await channel.send(embed=embed)

    # choose the item:
    selection = (await client.wait_for('message', check=check)).content

    target_item = ""

    if selection == '2':  # mob spawners
        target_item = "{MOB_SPAWNER"
    if log_type == "Skyblock":
        if selection == '3':  # mobcoin trophies
            target_item = "{MobCoin Trophy}"
        elif selection == '4':  # sell chest
            target_item = "{Sell Chest}"
        elif selection == '5':  # robots
            target_item = " Robot Spawn Egg}"
        elif selection == '6':  # infinity chests
            target_item = "{Infinity Chest}"
    elif log_type == "Prison":
        if selection == '3':  # robots
            target_item = " Robot Spawn Egg}"
        elif selection == '4':  # pickaxes
            target_item = "{DIAMOND_PICKAXE"

    await channel.send("Commencing...")
    results_file, amount = filescrapping.trade_logs(contents, mode, target_item, sender, receiver)

    info.current_params = [mode, target_item, sender, receiver]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Trades"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Amount of Trades In " + str(mode) + " Mode:",
                    value=str(amount), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Trading Logs and found " + str(amount) + " results", results_file])


async def vault(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    username = ""
    x_cor = ""
    z_cor = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Search By Username:", value="1", inline=False)
    embed.add_field(name="Search All:", value="2", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Username"
        await channel.send("Please enter the IGN that you are interested in")
        username = (await client.wait_for('message', check=check)).content
    elif mode == '2':
        mode = "All"

    await channel.send("Do you want to search by island coordinates? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Enter the X island coordinate now")
        x_cor = (await client.wait_for('message', check=check)).content
        await channel.send("Enter the Z island coordinate now")
        z_cor = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.vault_logs(contents, mode, username, x_cor, z_cor)

    info.current_params = [mode, username, x_cor, z_cor]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Vault Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Vault Logs Captured In " + str(mode) + " Mode:",
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Vault Logs and found " + str(total) + " results", results_file])


async def auction(contents, roles, user, info):
    username = ""
    channel = client.get_channel(the_channel_id)
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Is Auctioning Mode:", value="1", inline=False)
    embed.add_field(name="Has Purchased Mode:", value="2", inline=False)
    embed.add_field(name="Has Removed Mode:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Is Auctioning"
    elif mode == '2':
        mode = "Has Purchased"
    elif mode == '3':
        mode = "Has Removed"
    else:
        await channel.send("That was not an option!")

    await channel.send("Do you want to search by IGN? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please enter the IGN you want to search for")
        username = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.auction_logs(contents, mode.lower(), username)

    info.current_params = [mode.lower(), username]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Auction Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Auction Logs Captured In " + str(mode) + " Mode:",
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Auction Logs and found " + str(total) + " results", results_file])


async def drops(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Dropping:", value="1", inline=False)
    embed.add_field(name="Picking Up:", value="2", inline=False)
    embed.add_field(name="Both:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Dropped"
    elif mode == '2':
        mode = "Picked Up"
    elif mode == '3':
        mode = "Both"
    else:
        await channel.send("That was not an option!")

    # select based on realm
    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select What To Search For:",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Everything:", value="1", inline=False)
    embed.add_field(name="Mob Spawners:", value="2", inline=False)
    if log_type == "Skyblock":
        embed.add_field(name="Mobcoin Trophies", value="3", inline=False)
        embed.add_field(name="Sell Chests", value="4", inline=False)
        embed.add_field(name="Robots", value="5", inline=False)
        embed.add_field(name="Infinity Chests", value="6", inline=False)
    elif log_type == "Prison":
        embed.add_field(name="Robots", value="3", inline=False)
        embed.add_field(name="Pickaxes", value="4", inline=False)
    await channel.send(embed=embed)

    # choose the item:
    selection = (await client.wait_for('message', check=check)).content
    target_item = ""

    if selection == '1': # everything
        target_item = ""
    elif selection == '2': # mob spawners
        target_item = "MOB_SPAWNER"
        spawners = True
    elif log_type == "Skyblock":
        if selection == '3': # mobcoin trophies
            target_item = "| MobCoin Trophy |"
        elif selection == '4': # sell chest
            target_item = "| Sell Chest |"
        elif selection == '5': # robots
            target_item = " Robot Spawn Egg |"
        elif selection == '6': # infinity chests
            target_item = "| Infinity Chest |"
    elif log_type == "Prison":
        if selection == '3': # robots
            target_item = " Robot Spawn Egg |"
        elif selection == '4': # pickaxes
            target_item = "{DIAMOND_PICKAXE"

    if selection != '2':
        spawners = False


    await channel.send("Do you want to search by IGN? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please enter the IGN you want to search for")
        username = (await client.wait_for('message', check=check)).content
    else:
        username = ""

    world = ""
    x_cor = ""
    z_cor = ""

    if log_type == "Factions":
        embed = discord.Embed(
            colour=COLOR
        )
        embed.set_author(name="Select An Option",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="All Worlds", value="1", inline=False)
        embed.add_field(name="Overworld", value="2", inline=False)
        embed.add_field(name="Nether", value="3", inline=False)
        embed.add_field(name="End", value="4", inline=False)
        embed.add_field(name="Red", value="5", inline=False)
        embed.add_field(name="Grey", value="6", inline=False)
        embed.add_field(name="Clay", value="7", inline=False)
        embed.add_field(name="Sun", value="8", inline=False)
        embed.add_field(name="Crystal", value="9", inline=False)
        embed.add_field(name="Cherry", value="10", inline=False)
        embed.add_field(name="Dark", value="11", inline=False)

        await channel.send(embed=embed)
        num = (await client.wait_for('message', check=check)).content

        if num == '1': # all worlds
            world = ""
        elif num == '2':
            await channel.send("Overworld Selected!")
            world = "at world"
        elif num == '3':
            await channel.send("Nether Selected!")
            world = "at Nether"
        elif num == '4':
            await channel.send("End Selected!")
            world = "at End"
        elif num == '5':
            await channel.send("Red Selected!")
            world = "at red_flat"
        elif num == '6':
            await channel.send("Grey Selected!")
            world = "at grey"
        elif num == '7':
            await channel.send("Clay Selected!")
            world = "at clay_flat"
        elif num == '8':
            await channel.send("Sun Selected!")
            world = "at sunworld"
        elif num == '9':
            await channel.send("Crystal Selected!")
            world = "at crystalworld"
        elif num == '10':
            await channel.send("Cherry Selected!")
            world = "at cherryworld"
        else:
            await channel.send("Dark Selected!")
            world = "at darkworld"

    await channel.send("Do you want to search for drop/pick up logs within an 100 block radius? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please enter the X coordinate")
        x_cor = float((await client.wait_for('message', check=check)).content)

        await channel.send("Please enter the Z coordinate")
        z_cor = float((await client.wait_for('message', check=check)).content)

    await channel.send("Commencing...")
    results_file, total, spawner_file, total_users = filescrapping.drop_logs(contents, mode.lower(), spawners, username, world, x_cor, z_cor, target_item)

    info.current_params = [mode.lower(), spawners, username, world, x_cor, z_cor, target_item]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    if spawners and x_cor != "":
        embed.add_field(name="Spawners By User", value=str(total_users), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)
    if spawners and x_cor != "":
        await channel.send(file=spawner_file)

    await post_log(roles, [user + " completed Drop/Pickup Logs and found " + str(total) + " results", results_file])


async def voidchest(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    await channel.send("What is the faction name you're looking for? (Case Sensitive)")
    faction = (await client.wait_for('message', check=check)).content
    await channel.send("Commencing...")
    final = filescrapping.void_chest(contents, faction)

    info.current_params = [faction]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(faction + "'s VoidChest Deposits"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Deposits", value=final,
                    inline=False)
    await channel.send(embed=embed)

    await post_log(roles, [user + " completed Voidchest Logs\n" + final])


async def ftop(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    faction = ""
    placement = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="By Faction:", value="1", inline=False)
    embed.add_field(name="By Placement:", value="2", inline=False)
    embed.add_field(name="All:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        await channel.send("Please enter the faction your are looking for (Case Sensitive)")
        faction = (await client.wait_for('message', check=check)).content
        mode = "Faction F-Top"

    elif mode == '2':
        await channel.send("Please enter the placement your are looking for (1-15)")
        placement = (await client.wait_for('message', check=check)).content
        mode = "Placement F-Top"

    else:
        mode = "All F-Top"

    await channel.send("Commencing...")
    results_file, total = filescrapping.ftop_logs(contents, faction, placement)

    info.current_params = [faction, placement]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed FTOP Logs and found " + str(total) + " results", results_file])


async def land(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    faction = ""
    username = ""
    coordinates = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="By Faction", value="1", inline=False)
    embed.add_field(name="By Coordinates:", value="2", inline=False)
    embed.add_field(name="All:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        await channel.send("Please enter the faction your are looking for (Case Sensitive)")
        faction = (await client.wait_for('message', check=check)).content
        mode = "Faction Land"

    elif mode == '2':
        await channel.send("Please enter the coordinates your are looking for (Ex: 80,-25)")
        coordinates = (await client.wait_for('message', check=check)).content
        mode = "Coordinate Land"

    else:
        mode = "All Land"

    await channel.send("Do you want to search for a specific user? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please send the IGN you want to lookup")
        username = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.land_logs(contents, faction, username, coordinates)

    info.current_params = [faction, username, coordinates]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Claiming Land Logs and found " + str(total) + " results", results_file])


async def spawner_chunk(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    username = ""
    faction = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="By Username", value="1", inline=False)
    embed.add_field(name="By Faction:", value="2", inline=False)
    embed.add_field(name="All:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        await channel.send("Please enter the username your are looking for")
        username = (await client.wait_for('message', check=check)).content
        mode = "Username"

    elif mode == '2':
        await channel.send("Please enter the faction your are looking for")
        faction = (await client.wait_for('message', check=check)).content
        mode = "Faction"

    else:
        mode = "All"

    channel.send("Commencing...")
    results_file, total = filescrapping.spawner_chunk_logs(contents, username, faction)

    info.current_params = [username, faction]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Spawner Chunk Logs and found " + str(total) + " results", results_file])


async def updates(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    faction_raiding = ""
    faction_defending = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="By Two Factions:", value="1", inline=False)
    embed.add_field(name="By Raiding Faction:", value="2", inline=False)
    embed.add_field(name="By Defending Faction:", value="3", inline=False)
    embed.add_field(name="All:", value="4", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        await channel.send("Please enter the faction that is raiding")
        faction_raiding = (await client.wait_for('message', check=check)).content
        await channel.send("Please enter the faction that is defending")
        faction_defending = (await client.wait_for('message', check=check)).content
        mode = "By Two Factions"

    elif mode == '2':
        await channel.send("Please enter the faction that is raiding")
        faction_raiding = (await client.wait_for('message', check=check)).content
        mode = "By Raiding Faction"

    elif mode == '3':
        await channel.send("Please enter the faction that is defending")
        faction_defending = (await client.wait_for('message', check=check)).content
        mode = "By Defending Faction"

    else:
        mode = "All"

    channel.send("Commencing...")
    results_file, total = filescrapping.raid_updates(contents, faction_raiding, faction_defending)

    info.current_params = [faction_raiding, faction_defending]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Raiding Logs and found " + str(total) + " results", results_file])


async def lockdowns(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    faction_raiding = ""
    faction_defending = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="By Defending Faction:", value="1", inline=False)
    embed.add_field(name="All:", value="2", inline=False)

    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        await channel.send("Please enter the faction that is defending")
        faction_defending = (await client.wait_for('message', check=check)).content
        mode = "By Defending Faction"

    else:
        mode = "All"

    await channel.send("Commencing...")
    results_file, total = filescrapping.faction_lockdowns(contents, faction_defending)

    info.current_params = [faction_defending]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Lockdown Logs and found " + str(total) + " results", results_file])


async def coinflip(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    user1 = ""
    user2 = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Player vs. Player:", value="1", inline=False)
    embed.add_field(name="All With Player:", value="2", inline=False)
    if log_type != "Factions":
        embed.add_field(name="Player vs. Server:", value="3", inline=False)

    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Player vs. Player"
        await channel.send("Please enter one of the player's IGN")
        user1 = (await client.wait_for('message', check=check)).content
        await channel.send("Please enter the other IGN")
        user2 = (await client.wait_for('message', check=check)).content
    elif mode == '2':
        mode = "All With Player"
        await channel.send("Please enter the IGN you want to lookup")
        user1 = (await client.wait_for('message', check=check)).content
    elif mode == '3' and log_type != "Factions":
        mode = "Player vs. Server"
        await channel.send("Please enter the IGN you want to lookup")
        user1 = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.coinflip(contents, user1, user2, mode, log_type)

    info.current_params = [user1, user2, mode, log_type]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Coinflip Logs and found " + str(total) + " results", results_file])


async def rps(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    user1 = ""
    user2 = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Player vs. Player:", value="1", inline=False)
    embed.add_field(name="All With Player:", value="2", inline=False)
    if log_type != "Factions":
        embed.add_field(name="Player vs. Server:", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Player vs. Player"
        await channel.send("Please enter one of the player's IGN")
        user1 = (await client.wait_for('message', check=check)).content
        await channel.send("Please enter the other IGN")
        user2 = (await client.wait_for('message', check=check)).content
    elif mode == '2':
        mode = "All With Player"
        await channel.send("Please enter the IGN you want to lookup")
        user1 = (await client.wait_for('message', check=check)).content
    elif mode == '3' and log_type != "Factions":
        mode = "Player vs. Server"
        await channel.send("Please enter the IGN you want to lookup")
        user1 = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")

    results_file, total = filescrapping.rps(contents, user1, user2, mode, log_type)

    info.current_params = [user1, user2, mode, log_type]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed RPS Logs and found " + str(total) + " results", results_file])


async def cegg(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    username = ""
    x_cor = ""
    z_cor = ""

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select An Option",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Placed Logs (used against block)", value="1", inline=False)
    embed.add_field(name="Threw Logs (used in air)", value="2", inline=False)
    embed.add_field(name="All Logs", value="3", inline=False)
    await channel.send(embed=embed)
    mode = (await client.wait_for('message', check=check)).content

    if mode == '1':
        mode = "Placed"
    elif mode == '2':
        mode = "Threw"
    elif mode == '3':
        mode = "All"

    world = ""
    await channel.send("Do you want to search for CEGGS by world? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select An Option",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Overworld", value="1", inline=False)
        embed.add_field(name="Nether", value="2", inline=False)
        embed.add_field(name="End", value="3", inline=False)
        embed.add_field(name="Red", value="4", inline=False)
        embed.add_field(name="Grey", value="5", inline=False)
        embed.add_field(name="Clay", value="6", inline=False)
        await channel.send(embed=embed)
        num = (await client.wait_for('message', check=check)).content

        if num == '1':
            await channel.send("Overworld Selected!")
            world = "{name=world}"
        elif num == '2':
            await channel.send("Nether Selected!")
            world = "{name=Nether}"
        elif num == '3':
            await channel.send("End Selected!")
            world = "{name=End}"
        elif num == '4':
            await channel.send("Red Selected!")
            world = "{name=red_flat}"
        elif num == '5':
            await channel.send("Grey Selected!")
            world = "{name=grey}"
        else:
            await channel.send("Clay Selected!")
            world = "{name=clay_flat}"

    await channel.send("Do you want to search for CEGGS within an 100 block radius? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please enter the X coordinate")
        x_cor = float((await client.wait_for('message', check=check)).content)

        await channel.send("Please enter the Z coordinate")
        z_cor = float((await client.wait_for('message', check=check)).content)

    await channel.send("Do you want to search for a specific user? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please send the IGN you want to lookup")
        username = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.cegg_logs(contents, username, mode.lower(), world, x_cor, z_cor)

    info.current_params = [username, mode.lower(), world, x_cor, z_cor]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name=(mode + " Logs"),
                     icon_url=BOT_IMAGE)
    embed.add_field(name=(mode + " Mode Logs:"),
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed CEGG Logs and found " + str(total) + " results", results_file])


async def balance(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    username = ""

    await channel.send("Do you want to search by IGN? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please send the IGN you want to lookup")
        username = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.balance_logs(contents, username)

    info.current_params = [username]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Balance Logs",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Total Count:",
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Balance Logs and found " + str(total) + " results", results_file])

async def tpa(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    tpa_to_user = ""
    tpa_from_user = ""
    mode = '0'

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Select A Mode",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="/tpa Logs", value="1", inline=False)
    embed.add_field(name="/tpahere Logs", value="2", inline=False)
    embed.add_field(name="Teleport Accept Logs", value="3", inline=False)
    await channel.send(embed=embed)
    selection = (await client.wait_for('message', check=check)).content

    if selection == '1':
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select A Mode",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Search for players who tpa'd to a user", value="1", inline=False)
        embed.add_field(name="Search for players who a user tpa'd to", value="2", inline=False)
        embed.add_field(name="Search for teleports between two players", value="3", inline=False)
        await channel.send(embed=embed)
        mode = selection + " " + (await client.wait_for('message', check=check)).content

        if mode == '1 1':
            await channel.send("Please send the IGN who you want to search for")
            tpa_to_user = (await client.wait_for('message', check=check)).content
        elif mode == '1 2':
            await channel.send("Please send the IGN who you want to search for")
            tpa_from_user = (await client.wait_for('message', check=check)).content
        elif mode == '1 3':
            await channel.send("Please send one of the IGNs here")
            tpa_to_user = (await client.wait_for('message', check=check)).content
            await channel.send("Please send the other IGN here")
            tpa_from_user = (await client.wait_for('message', check=check)).content

    elif selection == '2':
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select A Mode",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Search for /tpahere requests sent by a user", value="1", inline=False)
        embed.add_field(name="Search for /tpahere requests for a user", value="2", inline=False)
        await channel.send(embed=embed)
        mode = selection + " " + (await client.wait_for('message', check=check)).content

        await channel.send("Please send the IGN who you want to search for")
        tpa_to_user = (await client.wait_for('message', check=check)).content


    elif selection == '3':
        await channel.send("Do you want to search by IGN? Yes/No")
        if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
            await channel.send("Please send the IGN you want to lookup")
            tpa_to_user = (await client.wait_for('message', check=check)).content
        mode = '3'

    await channel.send("Commencing...")
    results_file, total = filescrapping.tpa_logs(contents, tpa_to_user, tpa_from_user, mode)

    info.current_params = [tpa_to_user, tpa_from_user, mode]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="TPA Logs",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Total Count:",
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed TPA Logs and found " + str(total) + " results", results_file])

async def crates(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    username = ""

    await channel.send("Would you like to search by username? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Please send the IGN you want to lookup")
        username = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")

    results_file, total = filescrapping.crate_logs(contents, username)

    info.current_params = [username]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="Crate Logs",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Total Count:",
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed Crate Logs and found " + str(total) + " results", results_file])

async  def chunkhopper(contents, roles, user, info):
    channel = client.get_channel(the_channel_id)
    x_cor = ""
    z_cor = ""

    await channel.send("Do you want to search by island coordinates? Yes/No")
    if (await client.wait_for('message', check=check)).content.lower().startswith("y"):
        await channel.send("Enter the X island coordinate now")
        x_cor = (await client.wait_for('message', check=check)).content
        await channel.send("Enter the Z island coordinate now")
        z_cor = (await client.wait_for('message', check=check)).content

    await channel.send("Commencing...")
    results_file, total = filescrapping.chunkhopper_logs(contents, x_cor, z_cor)

    info.current_params = [x_cor, z_cor]

    embed = discord.Embed(
        colour=COLOR
    )

    embed.set_author(name="ChunkHopper Logs",
                     icon_url=BOT_IMAGE)
    embed.add_field(name="Total Count:",
                    value=str(total), inline=False)
    await channel.send(embed=embed)
    await channel.send(file=results_file)

    await post_log(roles, [user + " completed ChunkHopper Logs and found " + str(total) + " results", results_file])


def list_start(log_type):
    if log_type == "Factions":
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select An Option",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Selling Transactions:", value="1", inline=False)
        embed.add_field(name="Selling Stats (Auto-Selling):", value="2", inline=False)
        embed.add_field(name="Withdrawals in File:", value="3", inline=False)
        embed.add_field(name="Deposits in File", value="4", inline=False)
        embed.add_field(name="MobCoin Balances of User:", value="5", inline=False)
        embed.add_field(name="Chat Logs", value="6", inline=False)
        embed.add_field(name="Messages From/Between Player(s)", value="7", inline=False)
        embed.add_field(name="/Pay Logs", value="8", inline=False)
        embed.add_field(name="Trading Logs", value="9", inline=False)
        embed.add_field(name="Auction House Logs", value="10", inline=False)
        embed.add_field(name="VoidChest Deposits From A Faction", value="11", inline=False)
        embed.add_field(name="Dropping and Picking Up Logs", value="12", inline=False)
        embed.add_field(name="F-Top Logs", value="13", inline=False)
        embed.add_field(name="Claiming and Unclaiming Logs", value="14", inline=False)
        embed.add_field(name="Spawner Chunk Logs", value="15", inline=False)
        embed.add_field(name="Raid Update Logs", value="16", inline=False)
        embed.add_field(name="Lockdown Logs", value="17", inline=False)
        embed.add_field(name="Coinflip Logs", value="18", inline=False)
        embed.add_field(name="RPS Logs", value="19", inline=False)
        embed.add_field(name="CEGG Logs", value="20", inline=False)
        embed.add_field(name="Balance Logs", value="21", inline=False)
        embed.add_field(name="TPA Logs", value="22", inline=False)
        embed.add_field(name="Crate Logs", value="23", inline=False)
        return embed

    elif log_type == "Skyblock":
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select An Option",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="To Shop Transactions:", value="1", inline=False)
        embed.add_field(name="From Shop Transactions:", value="2", inline=False)
        embed.add_field(name="Selling and Sell Chest Transactions:", value="3", inline=False)
        embed.add_field(name="Selling Stats (Auto-Selling):", value="4", inline=False)
        embed.add_field(name="Withdrawals in File:", value="5", inline=False)
        embed.add_field(name="Deposits in File", value="6", inline=False)
        embed.add_field(name="MobCoin Balances of User:", value="7", inline=False)
        embed.add_field(name="Chat Logs", value="8", inline=False)
        embed.add_field(name="Island Chat Messages", value="9", inline=False)
        embed.add_field(name="Messages From/Between Player(s)", value="10", inline=False)
        embed.add_field(name="/Pay Logs", value="11", inline=False)
        embed.add_field(name="Trading Logs", value="12", inline=False)
        embed.add_field(name="Island Vault Logs", value="13", inline=False)
        embed.add_field(name="Auction House Logs", value="14", inline=False)
        embed.add_field(name="Coinflip Logs", value="15", inline=False)
        embed.add_field(name="RPS Logs", value="16", inline=False)
        embed.add_field(name="Balance Logs", value="17", inline=False)
        embed.add_field(name="Dropping and Picking Up Logs", value="18", inline=False)
        embed.add_field(name="TPA Logs", value="19", inline=False)
        embed.add_field(name="Crate Logs", value="20", inline=False)
        embed.add_field(name="ChunkHopper Logs", value="21", inline=False)
        return embed

    elif log_type == "Prison":
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select An Option",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Selling Transactions:", value="1", inline=False)
        embed.add_field(name="Withdrawals in File:", value="2", inline=False)
        embed.add_field(name="Deposits in File", value="3", inline=False)
        embed.add_field(name="Island Vault Logs", value="4", inline=False)
        embed.add_field(name="Chat Logs", value="5", inline=False)
        embed.add_field(name="Island Chat Messages", value="6", inline=False)
        embed.add_field(name="Messages From/Between Player(s)", value="7", inline=False)
        embed.add_field(name="/Pay Logs", value="8", inline=False)
        embed.add_field(name="Trading Logs", value="9", inline=False)
        embed.add_field(name="Auction House Logs", value="10", inline=False)
        embed.add_field(name="Coinflip Logs", value="11", inline=False)
        embed.add_field(name="RPS Logs", value="12", inline=False)
        embed.add_field(name="Balance Logs", value="13", inline=False)
        embed.add_field(name="Dropping and Picking Up Logs", value="14", inline=False)
        embed.add_field(name="TPA Logs", value="15", inline=False)
        embed.add_field(name="Crate Logs", value="16", inline=False)
        return embed

    elif log_type == "Outlands":
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select An Option",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Messages From/Between Players:", value="1", inline=False)
        embed.add_field(name="Chat Logs:", value="2", inline=False)
        embed.add_field(name="TPA Logs", value="3", inline=False)
        embed.add_field(name="Crate Logs", value="4", inline=False)
        return embed

    elif log_type == "Robbery":
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="Select An Option",
                         icon_url=BOT_IMAGE)
        embed.add_field(name="Trading Logs:", value="1", inline=False)
        embed.add_field(name="Withdrawals in File:", value="2", inline=False)
        embed.add_field(name="Deposits in File", value="3", inline=False)
        embed.add_field(name="Chat Logs", value="4", inline=False)
        embed.add_field(name="Messages From/Between Player(s)", value="5", inline=False)
        embed.add_field(name="Dropping and Picking Up Logs", value="6", inline=False)
        embed.add_field(name="Coinflip Logs", value="7", inline=False)
        embed.add_field(name="RPS Logs", value="8", inline=False)
        embed.add_field(name="TPA Logs", value="9", inline=False)
        embed.add_field(name="Balance Logs", value="10", inline=False)
        embed.add_field(name="Crate Logs", value="11", inline=False)
        return embed

    else:
        embed = discord.Embed(
            colour=COLOR
        )

        embed.set_author(name="This type hasn't been setup yet!",
                         icon_url=BOT_IMAGE)
        return embed


def zip_contents(link):
    req = urllib.request.Request(url=str(link), headers=headers)
    url = urllib.request.urlopen(req)
    with zipfile.ZipFile(BytesIO(url.read())) as my_zip_file:
        for contained_file in my_zip_file.namelist():
            date = (((my_zip_file.open(contained_file).readlines()[0]).decode('utf-8')).split(" first"))
            contents = my_zip_file.open(contained_file).read().decode('utf-8')
            return contents
    # try:
    #     print(os.getcwd())
    #     urllib.request.urlretrieve(link, "LinkedFile123.zip")
    #     print("1")
    # except:
    #     print("Something went wrong!")
    #
    # with zipfile.ZipFile("LinkedFile123" + ".zip", 'r') as zip_ref:
    #     zip_ref.extractall("LinkedFile123")
    # print("2")
    # os.remove("LinkedFile123.zip")
    # myfile = open(os.getcwd() + "/LinkedFile123/" + os.listdir(os.getcwd() + "/LinkedFile123")[0], "r",
    #               encoding="utf8")
    # print("3")
    # contents = myfile.read()
    # myfile.close()
    # print("4")
    # os.remove(os.getcwd() + "/LinkedFile123/" + os.listdir(os.getcwd() + "/LinkedFile123")[0])
    # return contents

async def post_log(roles, messages_to_post):
    global past_url
    #admin_id = 741436561203265636
    #senior_id = 741436655562391616

    for role in roles:
        if "Admin" in role.name:
            color = discord.Colour.red()
            break
        else:
            color = discord.Colour.purple()


    text = "Click here to view the file"
    embed = discord.Embed(
        colour=color
    )
    embed.set_author(name=messages_to_post[0],
                     icon_url=BOT_IMAGE)
    if past_url != file_url: # in case a result doesn't have a file attached
        embed.description = f"[{text}]({file_url})"
    past_url = file_url

    await client.get_channel(741436655562391616).send(embed=embed) # always a str
    # if len(messages_to_post) > 1:
    #     with open(messages_to_post[1].filename, 'w+') as f:
    #         print(messages_to_post[1].filename)
    #         print(messages_to_post[1])
    #         f.close()
    #         await client.get_channel(channel_id).send(file=f)


async def update_leaderboard():
    await client.wait_until_ready()
    channel = client.get_channel(692132676366368798)

    while not client.is_closed():
        try:
            eastern = timezone('US/Eastern')
            # localized datetime
            loc_dt = datetime.now(eastern)
            date = loc_dt.strftime("%I:%M %p, %B %d, %Y")
            if loc_dt.strftime("%M") == "00": #  ensures updates posted on the hour

                # members = users.keys()
                # leaders = []
                # index = 2
                # for member in members:
                #     leaders.append(Leaderboard(member, leaderboardsheet.get_score(index)))
                #     index += 1
                # sorted_leaders = sorted(leaders, key=get_score, reverse=True)
                #for leader in sorted_leaders:
                #    await channel.send(leader.member + ": " + leader.score)
                names, scores = calculate_leaderboard()

                embed = discord.Embed(
                    colour=COLOR
                )

                embed.set_author(name=date + " Leaderboard",
                                 icon_url=BOT_IMAGE)

                for num in range(10): # 10 = how many people to display
                    #embed.add_field(name=str(num + 1) + ". " + sorted_leaders[num].member, value="Points: " + sorted_leaders[num].score, inline=False)
                    embed.add_field(name=str(num + 1) + ". " + names[num], value="Points: " + scores[num], inline=False)
                await channel.send(embed=embed)

                delta = timedelta(hours=1)
                next_hour = (loc_dt + delta).replace(microsecond=0, second=0, minute=0)
                wait_seconds = (next_hour - loc_dt).seconds
                await asyncio.sleep(wait_seconds)

            else:
                delta = timedelta(hours=1)
                next_hour = (loc_dt + delta).replace(microsecond=0, second=0, minute=0)
                wait_seconds = (next_hour - loc_dt).seconds
                await asyncio.sleep(wait_seconds)

        except Exception as e:
            print("Leaderboard Error: " + str(e))
            await channel.send("Error!")
            delta = timedelta(hours=1)
            now = datetime.now()
            next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)
            wait_seconds = (next_hour - now).seconds
            await asyncio.sleep(wait_seconds)

class Leaderboard:
    def __init__(self, member, score):
        self.member = member
        self.score = score

# def get_score(obj):
#     return int(obj.score)

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        #conn = sqlite3.connect(db_file)
        conn = MySQLdb.connect(host="sql5.freemysqlhosting.net", user="sql5393034", passwd="TmYpKAv8ZR", db="sql5393034")
        return conn
    except Error as e:
        print(e)

    return conn

def calculate_leaderboard():
    connection = create_connection()
    cursor = connection.cursor()
    names = []
    scores = []
    cursor.execute('SELECT * FROM user_scores ORDER BY score DESC')
    results = cursor.fetchall()
    for person in results:
        names.append(str(person[0]))
        scores.append(str(person[1]))

    connection.close()
    return names, scores

def get_score(user):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT score FROM user_scores WHERE name=%s""", [user])
    current_score = cursor.fetchone()[0]
    print(user + "'s score is: " + str(current_score))
    connection.close()
    return current_score

def update_score(user):
    connection = create_connection()
    cursor = connection.cursor()
    current_score = int(get_score(user))
    new_score = current_score + 1
    print(new_score)

    #params = (new_score, user)
    #cursor.execute("""UPDATE scores SET score = {} WHERE name = '{}'""".format(new_score, user))
    update_str = 'UPDATE user_scores SET score=' + str(new_score) + ' WHERE name="' + user +'"'
    cursor.execute(update_str)
    connection.commit()
    connection.close()

# @client.command()
# async def load(ctx, extension):
#     # extension = cog to load
#     ctx.send("Loaded!")
#     client.load_extension(f'cogs.{extension}')
#
#
# @client.command()
# async def unload(ctx, extension):
#     ctx.send("Unloaded!")
#     client.unload_extension(f'cogs.{extension}')
#
# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         client.load_extension(f'cogs.{filename[:-3]}')


#connection = sqlite3.connect('user_scores.db')
# connection = create_connection()
# cursor = connection.cursor()
client.loop.create_task(update_leaderboard())
client.run("KEY")
