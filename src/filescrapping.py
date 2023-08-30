__author__ = "Tucker"
__version__ = "0.0.1"

"""A group of methods used within Discord to help moderating Minecraft servers
while assisting to make log checking easier than ever"""

import discord
import os


###################################
# Stats of Selling Items to /Shop #
###################################

def to_purchases(file_contents):
    """Returns all number of sales to sections in /shop"""

    # Default Amounts:
    shop_counter = file_contents.count("/shop")
    sell_all_counter = file_contents.count("sold all")
    ores_shop_counter = file_contents.count("to ores shop")
    redstone_shop = file_contents.count("to redstone shop")
    vip_shop = file_contents.count("to vip shop")
    drops_shop = file_contents.count("to drops shop")
    farming_shop = file_contents.count("to farming shop")
    food_shop = file_contents.count("to food shop")
    blocks_shop = file_contents.count("to blocks shop")
    dyes_shop = file_contents.count("to dyes shop")

    total = ores_shop_counter + redstone_shop + vip_shop + drops_shop + farming_shop + \
            food_shop + blocks_shop + dyes_shop

    return sell_all_counter, shop_counter, ores_shop_counter, vip_shop, drops_shop, food_shop, redstone_shop, \
           blocks_shop, farming_shop, dyes_shop, total


####################################
# Stats of Buying Items from /Shop #
####################################

def from_purchases(file_text):
    """Returns all number of sales from sections in /shop"""

    # Default Amounts:
    ores_shop_counter = file_text.count("from ores shop")
    redstone_shop = file_text.count("from redstone shop")
    vip_shop = file_text.count("from vip shop")
    drops_shop = file_text.count("from drops shop")
    farming_shop = file_text.count("from farming shop")
    food_shop = file_text.count("from food shop")
    blocks_shop = file_text.count("from blocks shop")
    colored_blocks = file_text.count("from coloredblocks shop")
    combat_shop = file_text.count("from combat shop")
    dyes_shop = file_text.count("from dyes shop")
    potions_shop = file_text.count("from potions shop")

    total = ores_shop_counter + redstone_shop + vip_shop + drops_shop + farming_shop + \
            food_shop + blocks_shop + colored_blocks + combat_shop + dyes_shop + potions_shop

    return ores_shop_counter, redstone_shop, vip_shop, drops_shop, farming_shop, \
           food_shop, blocks_shop, colored_blocks, combat_shop, dyes_shop, potions_shop, total


#############################################
# Money Made by IGN from Shop and SellChest #
#############################################

def ign_transactions(file_text, username, gamemode):
    """Returns the amount of money earned from sales to /shop and from SellChests"""

    lines = file_text.split("\n")  # array of lines
    total_sum_shop = 0.00
    total_sum_sellchest = 0.00

    for line in lines:

        if gamemode == "Skyblock" and line.find(username) != -1 and line.find("[SellChest] Deposited") != -1:
            # Manipulates string to be raw number
            chest = line[0:line.find(' for ')]
            chest = chest[chest.find('$') + 1:]
            chest = chest.replace(',', '')
            total_sum_sellchest += float(chest)

        if (gamemode == "Skyblock" or gamemode == "Factions") and (
                line.find("[ShopGUIPlus] " + username + " sold all") != -1):
            # Manipulates string to be raw number:
            money = line[0:line.find('$')]
            money = money[money.rfind(' ') + 1:]
            money = money.replace(',', '')
            total_sum_shop += float(money)

        elif gamemode == "Prison" and line.find("[SERVERPrison] " + username + " sold") != -1:
            line = line[line.find("$") + 1:line.find(" with")]
            line = line.replace(',', '')
            total_sum_shop += float(line)

    output1 = str(round(total_sum_shop, 2))

    if gamemode == "Skyblock":
        output2 = str(round(total_sum_sellchest, 2))
        return output1, output2
    else:
        return output1


##################################
# Stats of Possible Auto-Sellers #
##################################

def seconds_between_times(first_time, second_time):
    # [14:32:54]
    first_splits = first_time.replace("[", "").replace("]", "").split(":")
    second_splits = second_time.replace("[", "").replace("]", "").split(":")

    first_seconds = (first_splits[0] * 3600) + (first_splits[1] * 60) + first_splits[2]
    second_seconds = (second_splits[0] * 3600) + (second_splits[1] * 60) + second_splits[2]

    return second_seconds - first_seconds # amount of seconds between


def auto_sell2(file_text, username, flag=False):
    lines = file_text.split("\n")


    # dictionary of people if flag mode

    if flag:
        class AutoSeller:
            def __init__(self, times_sold, total_money_made, avg_time_between_sells):
                self.times_sold = times_sold # array of timestamps
                self.total_money_made = total_money_made # float
                self.avg_time_between_sells = avg_time_between_sells # float

            def get_times_sold(self):
                return self.times_sold

            def get_total_money_made(self):
                return float(self.total_money_made)


        # THRESHOLDS:
        SELLS_NEEDED = 100
        MONEY_NEEDED = 1000000 # 1 mil
        TIME_BETWEEN_NEEDED = 1 #seconds
        TIME_SELLING_NEEDED = 10 # minutes

        all_users = {}
        index = 0

        for line in lines:
            if line.find(" [ShopGUIPlus] ") != -1 and line.find(" sold all ") != -1:
                splits = line.split(" ")
                ign = splits[4]
                money = float(splits[-4][0: -1].replace(",", "")) # removes the $ sign at the end and remove ,
                if ign not in all_users.keys():
                    all_users[ign] = AutoSeller(splits[0], money, 0.0) # default values

                else:
                    all_users[ign] = AutoSeller([all_users.get(ign).times_sold].append(splits[0]), float(all_users.get(ign).total_money_made) + money, seconds_between_times(all_users.get(ign).times_sold[index], splits[0]))

                index += 1




        for user in all_users.keys():
            sells = len(all_users.get(user).times_sold)
            first_sell = all_users.get(ign).times_sold[0]
            last_sell = all_users.get(ign).times_sold[-1]
            average_money = all_users.get(ign).total_money_made / sells





def auto_sell(file_text, username, flag_mode=False, start_time=000000, end_time=235959):
    """Returns selling statistics of a specific IGNs"""

    lines = file_text.split("\n")  # array of lines

    # Default Amounts:
    times_sold = 0
    times_restrict = 0
    total_money = 0.0
    average_money = 0.0
    differences_of_time = 0.0
    time_limit = 5  # checks for amount (secs)
    break_time = 30  # amount of seconds to from a sell to the next to be considered a break
    break_counter = 0
    times = []

    for line in lines:
        if line.find(" [ShopGUIPlus] " + username + " sold all ") != -1:
            # Manipulates string to raw number
            amount = line[0:line.find('$')]
            amount = amount[amount.rfind(' ') + 1:]
            amount = amount.replace(',', '')
            total_money += float(amount)

            time = line[1:line.find(']')]
            time = time.replace(':', '')

            times.append(int(time))
            times_restrict += 1

            times_sold += 1

    average_money = total_money / times_sold
    first_sell = str(times[0])  # First sell in log file
    last_sell = str(times[len(times) - 1])  # Last sell in log file

    # Splicing the times to hours, minutes, seconds:
    if len(first_sell) == 5:
        hours_fs = int(first_sell[0:1])
        mins_fs = int(first_sell[1:3])
        secs_fs = int(first_sell[3:6])
    else:
        hours_fs = int(first_sell[0:2])
        mins_fs = int(first_sell[2:4])
        secs_fs = int(first_sell[4:6])

    if len(last_sell) == 5:
        hours_ls = int(last_sell[0:1])
        mins_ls = int(last_sell[1:3])
        secs_ls = int(last_sell[3:6])
    else:
        hours_ls = int(last_sell[0:2])
        mins_ls = int(last_sell[2:4])
        secs_ls = int(last_sell[4:6])

    # Amount of hours, minutes, seconds:
    total_hours = hours_ls - hours_fs
    total_mins = mins_ls - mins_fs
    total_secs = secs_ls - secs_fs

    # Prevents negative numbers:
    if total_mins < 0:
        total_hours -= 1
        total_mins = 60 + total_mins

    if total_secs < 0:
        total_mins -= 1
        total_secs = 60 + total_secs

    total_hours = str(total_hours)
    total_mins = str(total_mins)
    total_secs = str(total_secs)

    # Cuts off outliers and narrows-down crucial times:
    for i in range(len(times)):
        # Removes times that offset data
        if i + 1 < len(times):

            if i + 2 < len(times):
                # Counts the amount of breaks IGN took selling:
                if times[i + 1] - times[i] - 41 >= break_time and times[i + 1] - times[i] != 41 and \
                        times[i + 1] - times[i] != 4041:
                    # print(times[i], times[i + 1]) # Prints out times for testing
                    break_counter += 1

                # Removes times from over 5 seconds from final list
                if times[i + 1] - times[i] > time_limit:
                    times.pop(i)

                if times[i + 1] - times[i] < 4141:  # Time between hours (190000 - 185959)
                    differences_of_time += times[i + 1] - times[i]

    # Prevents division by 0 errors:
    if times_restrict == 0:
        times_restrict = 1
    if differences_of_time == 0:
        differences_of_time = 1

    minutes_selling = differences_of_time / 60  # differences_of_time in seconds
    avg_time_sell = differences_of_time / times_restrict

    # If in flag auto-selling mode (function flag_autoseller):
    if flag_mode:
        if int(total_hours) >= 1 and differences_of_time / times_restrict <= 5 and total_money >= 10000000:
            return True
        else:
            return False

    else:
        output = str((username + ":",
                      "Total Money Earned: $" + str(total_money),
                      "Average Money Per Sell: $" + str(round(average_money, 2)),
                      "Time From Last Sell to First Sell: " + total_hours + " hours " + total_mins,
                      "minutes and " + total_secs + " seconds",
                      "Active Selling Time: " + str(round(minutes_selling, 2)) + " minutes",
                      "Average Time Between Sells: " + str(round(avg_time_sell, 2)) + " seconds",
                      "Amount of Breaks Selling: " + str(break_counter) + " breaks!"))

        output = output.replace("(", "")
        output = output.replace(")", "")
        output = output.replace(",", "")

        return output


###################################
# Stats of Potential Auto-Sellers #
###################################

def flag_autoseller(file_text, start_time=000000, end_time=235959):
    """Returns statistics of a potential auto-sellers"""
    igns = []  # Stores all the IGNs that need to be checked
    lines = file_text.split("\n")  # array of lines
    output = ""

    for line in lines:
        if line.find("[ShopGUIPlus]") != -1 and line.find(" sold all ") != -1:
            first_loc = line.find('s]')
            second_loc = line.find('sold')
            ign = line[first_loc + 3:second_loc - 1]  # Gets exact IGN

        if ign not in igns:
            igns.append(ign)

    # Checks if each IGN passes requirements and s their stats:
    for n in range(len(igns)):
        ign_check = auto_sell(file_text, igns[n], True)

        if ign_check:
            output += auto_sell(file_text, igns[n], False)
    return output


############################
# MobCoin Balances of IGNs #
############################

def mobcoin_balance(file_text, ign):
    """Returns the Amount of MobCoins a Player Had"""

    lines = file_text.split("\n")
    txt_file = open("MobCoin_Balances.txt", "w+")
    for line in lines:

        if line.find("[MobCoins] Balance of") != -1 and line.find(ign) != -1:
            # Finds IGN and Balance:
            index1 = line.find("of") + 3  # Begins at IGN
            index2 = line.find(".") + 3  # Ends in the hundredth place
            balance = line[index1:index2]

            # Finds Time:
            index_time1 = 1
            index_time2 = 9
            time = line[index_time1:index_time2]

            txt_file.write("MobCoins of " + balance + " at " + time + " EST\n")

    txt_file.close()
    txt_file = open("MobCoin_Balances.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "MobCoin_Balances.txt")

    return txt_file

#########################################################
# Adds top file and converts the file to a Discord File #
#########################################################

def add_first_line(first_line, file_name):
    with open(file_name, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(first_line.rstrip('\r\n') + '\n\n' + content)
        f.close()
        f = open(file_name, "r+")
        f = discord.File(f)
        f.close()
    return f

################################
# Withdrawals of Money and EXP #
################################

def withdrawals(file_text, type, log_type, ign='n'):
    """Returns Withdrawals of Money and EXP as well as the grand totals"""

    total_withdrawals = 0  # Sums total money or EXP
    lines = file_text.split("\n")
    txt_file = open("Withdrawals.txt", "w+")

    for line in lines:
        if line.find(" successful withdrawal ") != -1 and line.find(ign) != -1:

            # Gathers IGN if global:
            if ign == "n":
                index_name1 = line.find("draw]") + 6
                index_name2 = line.find(" has ")
                name = line[index_name1:index_name2]
            else:
                name = ign

            # Gathers Amount:
            index_amount1 = line.find("for amount ") + 12
            index_amount2 = line.find(" with ID ") - 1
            amount = line[index_amount1:index_amount2].replace("'", "")

            # Gathers Time:
            time = line[1:9]

            if line.find("'money'") != -1 and type == 'money':
                txt_file.write(name + " withdrew $" + amount + " at " + time + " EST\n")
                total_withdrawals += float(amount.replace(',', ''))

            elif line.find("'exp'") != -1 and type == 'exp':
                txt_file.write(name + " withdrew " + amount + " of EXP at " + time + " EST\n")
                total_withdrawals += float(amount.replace(',', ''))

            if log_type == "Prison" and type == 'tokens' and line.find("'tokens'") != -1:
                txt_file.write(name + " withdrew " + amount + " of tokens at " + time + " EST\n")
                total_withdrawals += float(amount.replace(',', ''))

    txt_file.close()
    txt_file = open("Withdrawals.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Withdrawals.txt")

    return txt_file, total_withdrawals


#############################
# Deposits of Money and EXP #
#############################

def deposits(file_text, type, log_type, ign='n'):
    """Returns Deposits of Money and EXP as well as the grand totals"""

    total_deposits = 0  # Sums total money or EXP
    lines = file_text.split("\n")
    txt_file = open("Deposits.txt", "w+")

    for line in lines:
        if (line.find(" valid withdrawable ") != -1 or line.find(" in the faction bank: ") != -1) and line.find(
                ign) != -1:
            # Gathers Time:
            time = line[0:10]

            if log_type == "Skyblock" or log_type == "Prison":
                # Gathers IGN if global:
                if ign == "n":
                    index_name1 = line.find("draw] ") + 6
                    index_name2 = line.find("has") - 1
                    name = line[index_name1:index_name2]
                else:
                    name = ign

                if type == 'money' and line.find("type 'arwdty-money'") != -1:
                    # Gathers Amount:
                    index_amount1 = line.find(" amount ") + 9
                    index_amount2 = line.find(".") + 3
                    amount = line[index_amount1:index_amount2].replace("'", "")

                    txt_file.write(time + " " + name + " deposited $" + amount + "\n")
                    total_deposits += float(amount.replace(',', ''))

            elif log_type == "Factions" and type == "money" and line.find(" in the faction bank: ") != -1:

                # Gathers IGN if global:
                if ign == "n":
                    index_name1 = line.find(".2] ") + 4
                    index_name2 = line.find("deposited") - 1
                    name = line[index_name1:index_name2]
                else:
                    name = ign

                # Gathers Amount:
                index_amount1 = line.find("deposited") + 10
                index_amount2 = line.find("in the") - 1
                amount = line[index_amount1:index_amount2].replace("'", "")

                txt_file.write(time + " " + name + " deposited $" + amount + "\n")
                total_deposits += float(amount.replace(',', ''))

            if (type == 'exp' or type == "tokens") and (
                    line.find("'arwdty-exp'") != -1 or line.find("'arwdty-tokens'") != -1):
                # Gathers IGN if global:
                if ign == "n":
                    index_name1 = line.find("draw] ") + 6
                    index_name2 = line.find("has") - 1
                    name = line[index_name1:index_name2]
                else:
                    name = ign

                # Gathers Amount:
                index_amount1 = line.find(" amount ") + 9
                index_amount2 = line.find(".") + 3
                amount = line[index_amount1:index_amount2].replace("'", "")
                if type == "exp":
                    txt_file.write(time + " " + name + " deposited " + amount + " of EXP\n")
                else:
                    txt_file.write(time + " " + name + " deposited " + amount + " of tokens\n")
                total_deposits += float(amount.replace(',', ''))

    txt_file.close()
    txt_file = open("Deposits.txt", "r")  # updates file's contents
    txt_file = discord.File(txt_file)
    txt_file = add_first_line(lines[0], "Deposits.txt")


    return txt_file, total_deposits


##############################
# Messages Between Player(s) #
##############################

def gather_messages(file_text, user1, user2):
    lines = file_text.split("\n")
    total = 0
    txt_file = open(user1 + " and " + user2 + " Messages.txt", "w+")

    if user2 == "": # One person logs
        for line in lines:
            if user1.lower() in line.lower():
                time = line[0:10]
                lower_line = line.lower()
                if user1.lower() + " issued server command: " in lower_line:
                    if lower_line.find(" /msg ") != -1 or \
                        lower_line.find(" /message ") != -1 or \
                        lower_line.find(" /m ") != -1 or \
                        lower_line.find(" /tell ") != -1 or \
                        lower_line.find(" /w ") != -1 or \
                        lower_line.find(" /whisper ") != -1:

                        txt_file.write(time + " " + line[line.find("/INFO]:") + 8:] + "\n")
                        total += 1

                if line.lower().find(" [reply] " + user1.lower()) != -1:
                    txt_file.write(time + line[line.find(" [Reply] "): ] + "\n")
                    total += 1

    else: # Two person logs
        for line in lines:
            if user1.lower() in line.lower() and user2.lower() in line.lower():
                time = line[0:10]
                lower_line = line.lower()
                if " issued server command: " in line:
                    if lower_line.find(" /msg ") != -1 or \
                        lower_line.find(" /message ") != -1 or \
                        lower_line.find(" /m ") != -1 or \
                        lower_line.find(" /tell ") != -1 or \
                        lower_line.find(" /w ") != -1 or \
                        lower_line.find(" /whisper ") != -1:

                        txt_file.write(time + " " + line[line.find("/INFO]:") + 8:] + "\n")
                        total += 1

                if line.find(" [Reply] ") != -1:
                    txt_file.write(time + line[line.find(" [Reply] "):] + "\n")
                    total += 1

    txt_file.close()
    txt_file = open(user1 + " and " + user2 + " Messages.txt", "r")  # updates file's contents
    txt_file = discord.File(txt_file)
    txt_file.close()
    return txt_file, total



message_replied_to = False

def gather_messages2(file_text, user1, user2):
    # Two person message logs
    print("User1: " + user1)
    print("User2: " + user2)
    lines = file_text.lower().split("\n")
    if user2 != "":
        member_dict = {}
        last_reply = ""
        total = 0
        txt_file = open(user1 + " and " + user2 + " Messages.txt", "w+")

        for line in lines:
            if " issued server command: " in line and (user1.lower() in line or user2.lower() in line):
                time = line[0:10]
                if line.find(" /msg ") != -1 or \
                    line.find(" /message ") != -1 or \
                    line.find(" /m ") != -1 or \
                    line.find(" /tell ") != -1 or \
                    line.find(" /w ") != -1 or \
                    line.find(" /whisper ") != -1 or \
                    line.find(" /r ") != -1 or \
                    line.find(" /reply ") != -1:

                    user = line[line.find("/info]:") + 8:line.find("issued server") - 1].lower()  # gets the IGN

                    if " /r" not in line.lower() and user1.lower() in line and user2.lower() in line:
                        last_reply = line[line.find(" command: ") + 10:]  # gets the IGN
                        last_reply = last_reply[last_reply.find(" ") + 1:]
                        last_reply = last_reply[0:last_reply.find(" ")].lower() # BBC_BigBlackCar Fishy_Slap

                        if user in member_dict.keys():
                            member_dict.pop(user) # primed for replacement

                        if last_reply in member_dict.keys():
                            member_dict.pop(last_reply)

                        member_dict[user] = last_reply # replacement
                        member_dict[last_reply] = user

                        txt_file.write(time + " " + line[line.find("/info]:") + 8:] + "\n")
                        total += 1

                    if " /r" in line and (user1.lower() in line or user2.lower() in line): # if the message is a reply:
                        try:
                            last_reply = member_dict.get(user)
                        except Exception as e:
                            last_reply = "Unknown User"

                        if last_reply == "Unknown User" or last_reply == user1.lower() or last_reply == user2.lower():
                            txt_file.write(time + " Reply to " + last_reply + ": " + line[line.find("/info]:") + 8:] + "\n")
                            total += 1

        txt_file.close()
        txt_file = open(user1 + " and " + user2 + " Messages.txt", "r")  # updates file's contents
        txt_file = discord.File(txt_file)
        txt_file.close()
        return txt_file, total

    else:
        """Returns all the messages sent from an IGN"""
        member_dict = {}
        last_reply = ""
        total = 0
        txt_file = open(user1 + " Messages.txt", "w+")

        for line in lines:
            if user.lower() + " issued server command: " in line:
                time = line[0:10]
                if line.find(" /msg ") != -1 or \
                        line.find(" /message ") != -1 or \
                        line.find(" /m ") != -1 or \
                        line.find(" /tell ") != -1 or \
                        line.find(" /w ") != -1 or \
                        line.find(" /whisper ") != -1 or \
                        line.find(" /r ") != -1 or \
                        line.find(" /reply ") != -1:

                    user = line[line.find("/info]:") + 8:line.find("issued server") - 1].lower()  # gets the IGN

                    if " /r" not in line.lower() and user1.lower() in line:
                        last_reply = line[line.find(" command: ") + 10:]  # gets the IGN
                        last_reply = last_reply[last_reply.find(" ") + 1:]
                        last_reply = last_reply[0:last_reply.find(" ")].lower()  # BBC_BigBlackCar Fishy_Slap

                        if user in member_dict.keys():
                            member_dict.pop(user)  # primed for replacement

                        if last_reply in member_dict.keys():
                            member_dict.pop(last_reply)

                        member_dict[user] = last_reply  # replacement
                        member_dict[last_reply] = user

                        txt_file.write(time + " " + line[line.find("/info]:") + 8:] + "\n")
                        total += 1

                    if " /r" in line and (
                            user1.lower() in line):  # if the message is a reply:
                        try:
                            last_reply = member_dict.get(user)
                        except Exception as e:
                            last_reply = "Unknown User"

                        if last_reply == "Unknown User" or last_reply == user1.lower() and user1.lower():
                            txt_file.write(
                                time + " Reply to " + last_reply + ": " + line[line.find("/info]:") + 8:] + "\n")
                            total += 1

        txt_file.close()
        txt_file = open(user1 + " Messages.txt", "r")  # updates file's contents
        txt_file = discord.File(txt_file)
        txt_file.close()
        return txt_file, total



def find_reply(lines, time, username, username2):
    global message_replied_to

    last_reply = ""
    index = 0

    for s in lines:
        if time in s:
            break
        index += 1

    t_lines = lines[:index]

    username = username.lower()
    username2 = username2.lower()

    for i in range(len(t_lines) - 1, -1, -1):
        line = t_lines[i].lower()
        if username in line or username2 in line:
            upper_line = t_lines[i]

            if line.find(" issued server command: /msg " + username) != -1 or \
                    line.find(" issued server command: /message " + username) != -1 or \
                    line.find(" issued server command: /m " + username) != -1 or \
                    line.find(" issued server command: /tell " + username) != -1 or \
                    line.find(" issued server command: /w " + username) != -1 or \
                    line.find(" issued server command: /whisper " + username) != -1:

                last_reply = upper_line[
                             upper_line.find("/INFO]:") + 8:upper_line.find("issued server") - 1]  # gets the IGN
                break

            elif line.find(" issued server command: /msg " + username2) != -1 or \
                    line.find(" issued server command: /message " + username2) != -1 or \
                    line.find(" issued server command: /m " + username2) != -1 or \
                    line.find(" issued server command: /tell " + username2) != -1 or \
                    line.find(" issued server command: /w " + username2) != -1 or \
                    line.find(" issued server command: /whisper " + username2) != -1:

                last_reply = upper_line[upper_line.find(" command: ") + 10:]  # gets the IGN
                last_reply = last_reply[last_reply.find(" ") + 1:]
                last_reply = last_reply[0:last_reply.find(" ")]
                break


        if last_reply != "":
            return last_reply
        else:
            return "Unknown User"


#########################################
# Ensures No Errors in Var latest_reply #
#########################################

def fix_reply(line):
    """Changes the last IGN to send a message to avoid interruptions from outside players"""

    temp_line = line
    index1 = temp_line.find(": /") + 2  # Finds the beginning of IGN
    temp_line = temp_line[index1:]
    temp_line2 = temp_line
    index_of_space = temp_line.find(" ") + 1  # Spaces after of chars between / and first letter in IGN
    index1 = index_of_space
    temp_line = temp_line[index1:]
    index2 = temp_line.find(" ")  # Finds the ending of IGN

    return temp_line2[index1:index2 + index_of_space]  # Returns IGN


def void_chest(file_text, faction):
    lines = file_text.split("\n")
    faction_amount = 0
    total_amount = 0

    for line in lines:
        if line.find("[SERVERFactions] [VoidChest] Deposited") != -1 and line.find(faction) != -1:
            amount = line[line.find("$") + 1:line.find(" for ")]
            amount = amount.replace(",", "")
            faction_amount += float(amount)

        if line.find("[SERVERFactions] [VoidChest] Deposited") != -1:
            amount = line[line.find("$") + 1:line.find(" for ")]
            amount = amount.replace(",", "")
            total_amount += float(amount)

    return (faction + " deposited $" + str(faction_amount) + " from VoidChests",
            "$" + str(total_amount) + " was deposited from VoidChests in this file")


def island_chat(file_text, coords):
    lines = file_text.split("\n")
    txt_file = open("Island Chat.txt", "w+")

    for line in lines:
        if line.find("INFO]: [Ireland] [IS CHAT]") != -1 and line.find(coords) != -1:
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("<"):] + "\n")

    txt_file.close()
    txt_file = open("Island Chat.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Island Chat.txt")

    return txt_file


def pay_logs(file_text, sender, receiver, mode):
    file_text = file_text.lower()
    lines = file_text.split("\n")
    txt_file = open("Payment Logs.txt", "w+")
    total_amount = 0
    count = 0

    d = {
        'k': 3,
        'K': 3,
        'm': 6,
        'M': 6,
        'b': 9,
        'B': 9,
        't': 12,
        'T': 12
    }

    for line in lines:
        if line.find(" issued server command: /pay") != -1:

            checker = line[line.find("command:") + 9:]
            if checker.count(" ") == 2:  # Makes sure there is a payment amount

                time = line[0:10]
                amount = line[line.rfind(" ") + 1:]
                amount = amount.replace(",", "")
                amount = amount.replace("$", "")
                if any(char.isdigit() for char in amount):

                    try:
                        if amount[-1] in d:
                            num, magnitude = amount[:-1], amount[-1]
                            amount = float(amount[0:len(amount) - 1]) * 10 ** d[magnitude]
                        else:
                            amount = float(amount)

                        if mode == "Both":
                            if line.find(sender.lower() + " issued server command: /pay " + receiver.lower()) != -1:
                                txt_file.write(time + " " + line[line.find("/info]:") + 8:] + "\n")
                                total_amount += amount
                                count += 1

                        elif mode == "Send Only":
                            if line.find(sender.lower() + " issued server command: /pay ") != -1:
                                txt_file.write(time + " " + line[line.find("/info]:") + 8:] + "\n")
                                total_amount += amount
                                count += 1

                        elif mode == "Receive Only":
                            if line.find("issued server command: /pay " + receiver.lower()) != -1:
                                txt_file.write(time + " " + line[line.find("/info]:") + 8:] + "\n")
                                total_amount += amount
                                count += 1

                        elif mode == "All":
                            if line.find("issued server command: /pay ") != -1:
                                txt_file.write(time + " " + line[line.find("/info]:") + 8:] + "\n")
                                total_amount += amount
                                count += 1

                    except:
                        pass

    txt_file.close()
    txt_file = open("Payment Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Payment Logs.txt")

    return txt_file, total_amount, count


def trade_logs(file_text, mode, target_item, sender="", receiver=""):
    lines = file_text.split("\n")
    txt_file = open("Trade Logs.txt", "w+")
    total_trades = 0

    for line in lines:
        if line.find("[SERVERTrades] Trade completed:") != -1 and line.find(target_item) != -1:

            time = line[0:10]
            if mode == "Both" and line.lower().find(
                    sender.lower() + " --> " + receiver.lower() + " for:") != -1 or line.lower().find(
                    receiver.lower() + " --> " + sender.lower() + " for:") != -1:
                txt_file.write(time + " " + line[line.find("completed:") + 11:] + "\n")
                total_trades += 1

            elif mode == "Send/Receive" and line.lower().find(sender.lower() + " --> ") != -1 or line.lower().find(
                    " --> " + receiver.lower() + " for:") != -1:
                txt_file.write(time + " " + line[line.find("completed:") + 11:] + "\n")
                total_trades += 1

            elif mode == "All":
                txt_file.write(time + " " + line[line.find("completed:") + 11:] + "\n")
                total_trades += 1

    txt_file.close()
    txt_file = open("Trade Logs.txt", "r")  # updates file's contents
    #txt_file = discord.File(txt_file)
    #txt_file.close()
    txt_file = add_first_line(lines[0], "Trade Logs.txt")

    return txt_file, total_trades


def chat_logs(file_text, mode, keyword, username, type):
    lines = file_text.split("\n")

    txt_file = open(mode + " Logs.txt", "w+")
    total_messages = 0

    for line in lines:
        if line.find("[Async Chat Thread - #") != -1 or (
                line.find("issued server command: /g ") != -1 and type == "Outlands"):
            time = line[0:10]
            if mode == "Keyword" and line.lower().find(keyword.lower()) != -1:
                txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
                total_messages += 1

            elif mode == "Username" and line.find("] " + username) != -1:
                txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
                total_messages += 1
            elif mode == "Both" and line.lower().find(keyword.lower()) != -1 and line.find("] " + username) != -1:
                txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
                total_messages += 1

    txt_file.close()
    txt_file = open(mode + " Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], mode + " Logs.txt")

    return txt_file, total_messages


def tpa_logs(file_text, tpa_to_user, tpa_from_user, mode):
    # if mode = 1, looking for people who tpa'd to a user
    # if mode = 2, looking for people a user tpa'd to
    # if mode = 3, looking for tpas between two users
    lines = file_text.split("\n")

    txt_file = open("TPA Logs.txt", "w+")
    total_messages = 0

    for line in lines:
        if mode == '1 1' and line.lower().find("/tpa " + tpa_to_user.lower()) != -1:
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
            total_messages += 1

        elif mode == '1 2' and line.lower().find(tpa_from_user.lower() + " issued server command: /tpa ") != -1:
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
            total_messages += 1

        elif mode == '1 3' and (line.lower().find(tpa_from_user.lower() + " issued server command: /tpa " + tpa_to_user.lower()) != -1 or\
                line.lower().find(tpa_to_user.lower() + " issued server command: /tpa " + tpa_from_user.lower()) != -1):
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
            total_messages += 1

        elif mode == '2 1' and line.lower().find(tpa_to_user.lower() + " issued server command: /tpahere ") != -1:
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
            total_messages += 1

        elif mode == '2 2' and line.lower().find(" issued server command: /tpahere " + tpa_to_user.lower()) != -1:
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
            total_messages += 1

        elif mode == '3' and (line.lower().find(tpa_to_user.lower() + " issued server command: /tpyes") != -1 or\
                              line.lower().find(tpa_to_user.lower() + " issued server command: /tpaccept") != -1):
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("INFO") + 7:] + "\n")
            total_messages += 1

    txt_file.close()
    txt_file = open("TPA Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "TPA Logs.txt")

    return txt_file, total_messages

def vault_logs(file_text, mode, username, x_cor, z_cor):
    check_coords = x_cor != ""
    lines = file_text.split("\n")
    txt_file = open("Vault Logs.txt", "w+")
    total_vault = 0

    for line in lines:
        if line.find("/INFO]: [Ireland] [VaultLog]") != -1:
            time = line[0:10]


            if mode == "Username":
                if line.lower().find(username.lower()) != -1:
                    if check_coords:
                        if line.find("(x=" + x_cor + ", z=" + z_cor + ")") != -1:
                            txt_file.write(time + " " + line[line.find("Log]") + 4:] + "\n")
                            total_vault += 1
                    else:
                        txt_file.write(time + " " + line[line.find("Log]") + 4:] + "\n")
                        total_vault += 1

            else:
                if check_coords:
                    if line.find("(x=" + x_cor + ", z=" + z_cor + ")") != -1:
                        txt_file.write(time + " " + line[line.find("Log]") + 4:] + "\n")
                        total_vault += 1
                else:
                    txt_file.write(time + " " + line[line.find("Log]") + 4:] + "\n")
                    total_vault += 1

    txt_file.close()
    txt_file = open("Vault Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Vault Logs.txt")

    return txt_file, total_vault


def auction_logs(file_text, mode, username=""):
    lines = file_text.split("\n")
    txt_file = open("Auction Logs.txt", "w+")
    total_ah = 0

    for line in lines:
        if line.find("/INFO]: [SERVERAuctionHouse]") != -1:
            time = line[0:10]

            if mode == "is auctioning":
                if line.find(mode) != -1:
                    if username != "":
                        if line.find(username) != -1:
                            txt_file.write(time + " " + line[line.find("House]") + 7:] + "\n")
                            total_ah += 1
                    else:
                        txt_file.write(time + " " + line[line.find("House]") + 7:] + "\n")
                        total_ah += 1

            elif mode == "has purchased":
                if line.find(mode) != -1:
                    if username != "":
                        if line.find(username) != -1:
                            txt_file.write(time + " " + line[line.find("House]") + 7:] + "\n")
                            total_ah += 1
                    else:
                        txt_file.write(time + " " + line[line.find("House]") + 7:] + "\n")
                        total_ah += 1

            elif mode == "has removed":
                if line.find(mode) != -1:
                    if username != "":
                        if line.find(username) != -1:
                            txt_file.write(time + " " + line[line.find("House]") + 7:] + "\n")
                            total_ah += 1
                    else:
                        txt_file.write(time + " " + line[line.find("House]") + 7:] + "\n")
                        total_ah += 1

    txt_file.close()
    txt_file = open("Auction Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Auction Logs.txt")

    return txt_file, total_ah




def drop_logs(file_text, mode, spawners, username, world, x_cor, z_cor, target_item):
    lines = file_text.split("\n")
    txt_file = open("Pickup Logs.txt", "w+")
    txt_file2 = open("User Spawners.txt", "w+")
    total_drop = 0
    total_users = 0
    players_with_spawners = {}

    for line in lines:
        if line.find("[Server thread/INFO]: [SERVERShared] [PDT]") != -1 and line.find(target_item) != -1 and line.find(world) != -1 and line.find(username) != -1:

            if mode == "dropped" and x_cor == "":

                if line.find(mode) != -1:
                    writing = drops_write(line, spawners, username)
                    if writing != "":
                        txt_file.write(writing)
                        total_drop += 1

            elif mode == "picked up" and x_cor == "":

                if line.find(mode) != -1:
                    writing = drops_write(line, spawners, username)
                    if writing != "":
                        txt_file.write(writing)
                        total_drop += 1

            elif mode == "both" and x_cor == "":
                writing = drops_write(line, spawners, username)
                if writing != "":
                    txt_file.write(writing)
                    total_drop += 1

            elif x_cor != "": # true if coords are enabled
                time = line[0:10]
                coordinate_lines = line.split(" ")
                x_val = coordinate_lines[len(coordinate_lines) - 3]
                x_val = int(x_val.replace("x", ""))
                z_val = coordinate_lines[len(coordinate_lines) - 1]
                z_val = int(z_val.replace("z", ""))

                if x_cor - 100 <= x_val <= x_cor + 100 and z_cor - 100 <= z_val <= z_cor + 100:
                    writing = drops_write(line, spawners, username)
                    if writing != "":
                        txt_file.write(writing)
                        total_drop += 1

            if spawners and x_cor != "" and line.find("MOB_SPAWNER") != -1:
                coordinate_lines = line.split(" ")
                x_val = coordinate_lines[len(coordinate_lines) - 3]
                x_val = int(x_val.replace("x", ""))
                z_val = coordinate_lines[len(coordinate_lines) - 1]
                z_val = int(z_val.replace("z", ""))
                if x_cor - 100 <= x_val <= x_cor + 100 and z_cor - 100 <= z_val <= z_cor + 100:

    
                    line_split = line.split(" ")
                    player = line_split[5]

                    amount_int = 8 
                    spawner_int = 12


                    if " dropped {" in line:
                        amount_int -= 1
                        spawner_int -= 1
                    amount_of_spawners = line_split[amount_int].replace("x", "").replace("{", "")
                    spawner_type = line_split[spawner_int].replace("§e", "")
                    finished_line = amount_of_spawners + " " + spawner_type
                    print(finished_line)

                    if player not in players_with_spawners.keys():
                        players_with_spawners[player] = finished_line
                    else:
                        if spawner_type not in players_with_spawners.get(player):
                            players_with_spawners[player] = players_with_spawners.get(player) + "," + finished_line
                        else:
                            all_player = players_with_spawners[player].split(",")
                            for i in range(len(all_player)):
                                if spawner_type in all_player[i - 1]:
                                    new_number = int(all_player[i - 1][0:all_player[i - 1].find(" ")])
                                    all_player[i - 1] = str(new_number + int(amount_of_spawners)) + " " + spawner_type
                                    break
                            all_text = ""
                            for value in all_player:
                                all_text += value + ","
                            players_with_spawners[player] = all_text[0:len(all_text) - 1]

    if spawners and x_cor != "":
        for player, value in players_with_spawners.items():
            txt_file2.write(player + ": " + value + "\n")
            total_users += 1

    txt_file2.close()
    txt_file2 = open("User Spawners.txt", "r")  # updates file's contents
    txt_file2 = add_first_line(lines[0], "User Spawners.txt")

    txt_file.close()
    txt_file = open("Pickup Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Pickup Logs.txt")

    return txt_file, total_drop, txt_file2, total_users


def drops_write(line, spawners, username):
    time = line[0:10]
    # IGN and looking for spawners
    if username != "":
        if line.lower().find(username.lower()) != -1 and spawners and line.find("MOB_SPAWNER") != -1:
            return time + " " + line[line.find("[PDT]") + 6:] + "\n"

        # IGN and not looking for spawners
        elif line.lower().find(username.lower()) != -1 and not spawners:
            return time + " " + line[line.find("[PDT]") + 6:] + "\n"
        else:
            return ""

    # No IGN and looking for spawners
    else:
        if spawners and line.find("MOB_SPAWNER") != -1:
            return time + " " + line[line.find("[PDT]") + 6:] + "\n"

        # No IGN and not looking for spawners
        elif not spawners:
            return time + " " + line[line.find("[PDT]") + 6:] + "\n"

        else:
            return ""


def ftop_logs(file_text, faction, placement):
    lines = file_text.split("\n")
    txt_file = open("F-Top Logs.txt", "w+")
    index = 0
    total_logs = 0

    for line in lines:
        if line.find("[FactionsTop] [FTop-Log]") != -1:
            time = line[0:10]
            # All FTop Logs:
            if faction == "" and placement == "":
                txt_file.write(time + " " + line[line.find("Log]") + 5:] + "\n")
                total_logs += 1

            # Faction Logs:
            elif faction != "":
                if line.find(faction) != -1:
                    txt_file.write(time + " " + line[line.find("Log]") + 5:] + "\n")
                    txt_file.write(time + " " + lines[index + 1][lines[index + 1].find("Log]") + 5:] + "\n")
                    total_logs += 1

            # Placement Logs:
            else:
                if line.find("#" + placement + " - ") != -1:
                    txt_file.write(time + " " + line[line.find("Log]") + 5:] + "\n")
                    txt_file.write(time + " " + lines[index + 1][lines[index + 1].find("Log]") + 5:] + "\n")
                    total_logs += 1

        index += 1  # Used for adding spawner amounts

    txt_file.close()
    txt_file = open("F-Top Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "F-Top Logs.txt")

    return txt_file, total_logs


def land_logs(file_text, faction, username, coordinates):
    lines = file_text.split("\n")
    txt_file = open("Claiming Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("[Factions v-U0.2.2]") != -1 and \
                (line.find("claimed land") != -1 or line.find("unclaimed land") != -1):

            time = line[0:10]

            # All Logs:
            if faction == "" and coordinates == "":
                if username == "":
                    txt_file.write(time + " " + line[line.find(".2]") + 4:] + "\n")
                    total_logs += 1
                else:
                    if line.find(username) != -1:
                        txt_file.write(time + " " + line[line.find(".2]") + 4:] + "\n")
                        total_logs += 1

            # Faction Logs:
            elif faction != "" and line.find(faction) != -1:
                if username == "":
                    txt_file.write(time + " " + line[line.find(".2]") + 4:] + "\n")
                    total_logs += 1
                elif line.find(username) != -1:
                    txt_file.write(time + " " + line[line.find(".2]") + 4:] + "\n")
                    total_logs += 1

            # Coordinate Logs:
            elif coordinates != "" and line.find(coordinates) != -1:
                if username == "":
                    txt_file.write(time + " " + line[line.find(".2]") + 4:] + "\n")
                    total_logs += 1
                elif line.find(username) != -1:
                    txt_file.write(time + " " + line[line.find(".2]") + 4:] + "\n")
                    total_logs += 1

    txt_file.close()
    txt_file = open("Claiming Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Claiming Logs.txt")

    return txt_file, total_logs


def spawner_chunk_logs(file_text, username, faction):
    lines = file_text.split("\n")
    txt_file = open("Spawner Chunk Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("[Factions v-U0.2.2]") != -1 and line.find("Spawner Chunk") != -1:
            time = line[0:10]

            # By Username
            if username != "":
                if line.find(username) != -1:
                    txt_file.write(time + " " + line[line.find(".2.2]") + 6:] + "\n")
                    total_logs += 1

            # By Faction
            elif faction != "":
                if line.find(faction) != -1:
                    txt_file.write(time + " " + line[line.find(".2.2]") + 6:] + "\n")
                    total_logs += 1

            # All
            else:
                txt_file.write(time + " " + line[line.find(".2.2]") + 6:] + "\n")
                total_logs += 1

    txt_file.close()
    txt_file = open("Spawner Chunk Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Spawner Chunk Logs.txt")

    return txt_file, total_logs


def raid_updates(file_text, faction_raiding, faction_defending):
    lines = file_text.split("\n")
    txt_file = open("Raid Updates.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("[Factions] [Raid Update]") != -1:
            time = line[0:10]

            # By Two Factions
            if faction_raiding != "" and faction_defending != "":
                if line.find(" by " + faction_raiding) != -1 and line.find("] " + faction_defending) != -1:
                    txt_file.write(time + " " + line[line.find("Update]") + 8:] + "\n")
                    total_logs += 1

            # By Raiding Faction
            elif faction_raiding != "":
                if line.find(" by " + faction_raiding) != -1:
                    txt_file.write(time + " " + line[line.find("Update]") + 8:] + "\n")
                    total_logs += 1

            # By Raiding Faction
            elif faction_defending != "":
                if line.find("] " + faction_defending) != -1:
                    txt_file.write(time + " " + line[line.find("Update]") + 8:] + "\n")
                    total_logs += 1

            # All
            else:
                txt_file.write(time + " " + line[line.find("Update]") + 8:] + "\n")
                total_logs += 1

    txt_file.close()
    txt_file = open("Raid Updates.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Raid Updates.txt")

    return txt_file, total_logs


def faction_lockdowns(file_text, faction_defending):
    lines = file_text.split("\n")
    txt_file = open("Lockdown Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("ockdown on " + faction_defending) != -1:
            time = line[0:10]
            txt_file.write(time + " " + line[line.rfind("]") + 2:] + "\n")
            total_logs += 1

    txt_file.close()
    txt_file = open("Lockdown Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Lockdown Logs.txt")

    return txt_file, total_logs


def coinflip(file_text, user1, user2, mode, log_type):
    if log_type == "Factions":
        file_text = file_text.replace("§6", "")
        file_text = file_text.replace("§8", "")
        file_text = file_text.replace("§l", "")
        file_text = file_text.replace("§c", "")
        file_text = file_text.replace("§e", "")

    lines = file_text.split("\n")
    txt_file = open("Coinflip Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("]: CF >> ") != -1:
            time = line[0:10]
            # Player vs. Server or All By Player:
            if user2 == "":
                if mode == "All With Player":
                    if line.find(user1) != -1:
                        txt_file.write(time + " " + line[line.find(">> ") + 3:] + "\n")
                        total_logs += 1
                else:
                    if line.find("The Server") != -1 and line.find(user1) != -1:
                        txt_file.write(time + " " + line[line.find(">> ") + 3:] + "\n")
                        total_logs += 1
            # Player vs. Player:
            else:
                if line.find(user1 + " has defeated " + user2) != -1:
                    txt_file.write(time + " " + line[line.find(">> ") + 3:] + "\n")
                    total_logs += 1

    txt_file.close()
    txt_file = open("Coinflip Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Coinflip Logs.txt")

    return txt_file, total_logs


def rps(file_text, user1, user2, mode, log_type):
    lines = file_text.split("\n")
    txt_file = open("RPS Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("[SERVERGambling] [RPS] Finished wager:") != -1:
            time = line[0:10]
            # Player vs. Server or All By Player:
            if user2 == "":
                if mode == "All With Player":
                    if line.find(user1) != -1:
                        txt_file.write(time + " " + line[line.find("wager:") + 7:] + "\n")
                        total_logs += 1
                else:
                    if line.find(user1 + " vs The Server") != -1:
                        txt_file.write(time + " " + line[line.find("wager:") + 7:] + "\n")
                        total_logs += 1
            # Player vs. Player:
            else:
                if line.find(user1 + " vs " + user2) != -1:
                    txt_file.write(time + " " + line[line.find("wager:") + 7:] + "\n")
                    total_logs += 1

    txt_file.close()
    txt_file = open("RPS Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "RPS Logs.txt")

    return txt_file, total_logs



def cegg_logs(file_text, username, mode, world, x_cor, z_cor):
    lines = file_text.split("\n")
    txt_file = open("CEGG Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("[Server thread/INFO]: [SERVERFactions] [CreeperEgg]") != -1 and line.find(world) != -1:
            time = line[0:10]

            if mode == "placed" and x_cor == "":
                if line.find(username + " used against block") != -1:
                    txt_file.write(time + " " + line[line.find("Egg]") + 5:] + "\n")
                    total_logs += 1
            elif mode == "threw" and x_cor == "":
                if line.find(username + " used in air") != -1:
                    txt_file.write(time + " " + line[line.find("Egg]") + 5:] + "\n")
                    total_logs += 1
            elif mode == "all" and x_cor == "":
                txt_file.write(time + " " + line[line.find("Egg]") + 5:] + "\n")
                total_logs += 1

            elif x_cor != "" and z_cor != "":
                tline = line.replace("x=", "")
                tline = tline.replace("z=", "")
                coordinate_lines = tline.split(",")
                x_val = float(coordinate_lines[1])
                z_val = float(coordinate_lines[3])

                if x_cor - 100 <= x_val <= x_cor + 100 and z_cor - 100 <= z_val <= z_cor + 100:
                    if mode == "all":
                        txt_file.write(time + " " + line[line.find("Egg]") + 5:] + "\n")
                        total_logs += 1
                    elif mode == "placed":
                        if line.find(username + " used against block") != -1:
                            txt_file.write(time + " " + line[line.find("Egg]") + 5:] + "\n")
                            total_logs += 1
                    elif mode == "threw":
                        if line.find(username + " used in air") != -1:
                            txt_file.write(time + " " + line[line.find("Egg]") + 5:] + "\n")
                            total_logs += 1

    txt_file.close()
    txt_file = open("CEGG Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "CEGG Logs.txt")

    return txt_file, total_logs


def balance_logs(file_text, username):
    lines = file_text.split("\n")
    txt_file = open("Balance Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("[SERVERShared] [BalanceLog] " + username) != -1:
            time = line[0:10]
            txt_file.write(time + " " + line[line.find("Log]") + 5:] + "\n")
            total_logs += 1

    txt_file.close()
    txt_file = open("Balance Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Balance Logs.txt")

    return txt_file, total_logs

def filter_file(contents, filter, is_all, mode):
    title = filter.replace("/", "")
    filtered_file = open(title + " Filter.txt", "w+")
    lines = contents.split("\n")
    filtered_file.write(lines[0] + "\n\n")

    if is_all:
        filter_result = [x.strip() for x in filter.split('&')] # AND
    else:
        filter_result = [x.strip() for x in filter.split('|')] # OR
    for line in lines:
        if is_all and mode:
            if all(x in line.lower() for x in filter_result):
                filtered_file.write(line + "\n")
        elif mode:
            if any(x in line.lower() for x in filter_result):
                filtered_file.write(line + "\n")

        elif is_all and not mode:
            if all(x not in line.lower() for x in filter_result):
                filtered_file.write(line + "\n")
        else:
            if any(x not in line.lower() for x in filter_result):
                filtered_file.write(line + "\n")

    filtered_file.close()
    filtered_file = open(title + " Filter.txt", "r")  # updates file's contents
    filtered_file = discord.File(filtered_file)
    filtered_file.close()
    return filtered_file

def crate_logs(file_text, username):
    # "EmeraldRaven just won " and "[SERVERCore]"

    lines = file_text.split("\n")
    txt_file = open("Crate Logs.txt", "w+")
    total_logs = 0
    # [Crates] Dispatching command for EmeraldRaven

    for line in lines:
        if line.lower().find("[crates] dispatching command for " + username.lower()) != -1 or (line.find(username.lower() + " just won ") != -1 and line.lower().find("[SERVERcore]") != -1):
            time = line[0:10]
            txt_file.write(time + " " + ' '.join([str(elem) for elem in line.split(" ")[3:]]) + "\n")
            total_logs += 1

    txt_file.close()
    txt_file = open("Crate Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "Crate Logs.txt")

    return txt_file, total_logs

def chunkhopper_logs(contents, x_cor, z_cor):
    lines = contents.split("\n")
    txt_file = open("ChunkHopper Logs.txt", "w+")
    total_logs = 0

    for line in lines:
        if line.find("[SERVERShared] [ChunkHopper-AutoSell] Deposited $") != -1:
            time = line[0:10]
            if x_cor != "":
                txt_file.write(time + " " + ' '.join([str(elem) for elem in line.split(" ")[2:]]))
                total_logs += 1
            else:
                if line.find(" for " + x_cor + "," + z_cor) != -1:
                    txt_file.write(time + " " + ' '.join([str(elem) for elem in line.split(" ")[2:]]))
                    total_logs += 1

    txt_file.close()
    txt_file = open("ChunkHopper Logs.txt", "r")  # updates file's contents
    txt_file = add_first_line(lines[0], "ChunkHopper Logs.txt")

    return txt_file, total_logs

spawner_track_lines = []
def spawner_tracker(contents, starting_line):


    info_lines = starting_line.split(" ")

    username = info_lines[0]
    #print("Username: " + username)

    x_val = info_lines[len(info_lines) - 3]
    x_val = int(x_val.replace("x", ""))

    z_val = info_lines[len(info_lines) - 1]
    z_val = int(z_val.replace("z", ""))

    spawner_type = info_lines[5].replace("§e", "")
    #print("Spawner Type: " + spawner_type)
    track_spawner_movement(contents.split("\n"), username, spawner_type)

    txt_file = open("Spawner Tracker.txt", "w+")
    for log in spawner_track_lines:
        txt_file.write(log + "\n")

    txt_file.close()
    txt_file = open("Spawner Tracker.txt", "r")  # updates file's contents
    txt_file = add_first_line(contents.split("\n")[0], "Spawner Tracker.txt")

    return txt_file

def track_spawner_movement(lines, username, spawner_type):
    global spawner_track_lines
    # Dropped Them:
    mode = ""
    append_line = ""
    for line in lines:
        if username in line and spawner_type in line:
            line_info = line.split(" ")
            if " picked up " in line:
                mode = "Drop/Pickup"
                username = line_info[4]

            elif " [SERVERAuctionHouse] " in line:
                mode = "Auction"
                username = line_info[4]

            elif " [SERVERTrades] " in line:
                mode = "Trade"
                username = line.info[4]

            append_line = line[line.find("/INFO]:") + 8:]

            # print("Username2: " + username)
            time = line[0:10]
            spawner_track_lines.append(time + " " + append_line)
            try:
                new_lines = lines[lines.find(line) + 1:]
                track_spawner_movement(new_lines, username, spawner_type)
            except Exception as e:
                return

        elif username in line and ("/f chest" in line or "/f vault" in line or "/trash" in line or "/bin" in line or "/ci" in line):
            append_line = line[line.find("/INFO]:") + 8:]

            #print("Username2: " + username)
            time = line[0:10]
            spawner_track_lines.append(time + " " + append_line)
            try:
                new_lines = lines[lines.find(line) + 1:]
                track_spawner_movement(new_lines, username, spawner_type)
            except Exception as e:
                return