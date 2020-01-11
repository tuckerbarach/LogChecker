__author__ = "Tucker / SwagRuler"
__version__ = "0.0.1"

"""A group of methods used within Discord to help moderating Minecraft servers
while assisting to make log checking easier than ever"""


###################################
# Stats of Selling Items to /Shop #
###################################

def to_purchases(file, mode='r'):
    """Returns all number of sales to sections in /shop"""

    with open(file, mode) as text:

        # Default Amounts:
        shop_counter = 0
        sell_all_counter = 0
        ores_shop_counter = 0
        redstone_shop = 0
        vip_shop = 0
        drops_shop = 0
        farming_shop = 0
        food_shop = 0
        blocks_shop = 0
        dyes_shop = 0

        # Adds 1 to each counter if keyword found:
        for line in text:

            if line.find("sold all") != -1:
                sell_all_counter += 1

            if line.find("/shop") != -1:
                shop_counter += 1

            if line.find("to ores shop") != -1:
                ores_shop_counter += 1

            elif line.find("to vip shop") != -1:
                vip_shop += 1

            elif line.find("to drops shop") != -1:
                drops_shop += 1

            elif line.find("to food shop") != -1:
                food_shop += 1

            elif line.find("to redstone shop") != -1:
                redstone_shop += 1

            elif line.find("to blocks shop") != -1:
                blocks_shop += 1

            elif line.find("to farming shop") != -1:
                farming_shop += 1

            elif line.find("to dyes shop") != -1:
                dyes_shop += 1

        total = ores_shop_counter + redstone_shop + vip_shop + drops_shop + farming_shop + \
                food_shop + blocks_shop + dyes_shop

        return ("\nSell All: " + str(sell_all_counter), "\n/shop: " + str(shop_counter),
                "\nTo Ores Shop: " + str(ores_shop_counter), "\nTo VIP Shop: " + str(vip_shop),
                "\nTo Drops Shop: " + str(drops_shop), "\nTo Food Shop: " + str(food_shop),
                "\nTo Redstone Shop: " + str(redstone_shop), "\nTo Block Shop: " + str(blocks_shop),
                "\nTo Farming Shop: " + str(farming_shop), "\nTo Dyes/Flowers Shop: " + str(dyes_shop),
                "\nTotal To Buys: " + str(total))


####################################
# Stats of Buying Items from /Shop #
####################################

def from_purchases(file, mode='r'):
    """Returns all number of sales from sections in /shop"""

    with open(file, mode) as text:

        # Default Amounts:
        ores_shop_counter = 0
        redstone_shop = 0
        vip_shop = 0
        drops_shop = 0
        farming_shop = 0
        food_shop = 0
        blocks_shop = 0
        colored_blocks = 0
        combat_shop = 0
        dyes_shop = 0
        potions_shop = 0

        # Adds 1 to each counter if keyword found:
        for line in text:

            if line.find("from blocks shop") != -1:
                blocks_shop += 1

            elif line.find("from farming shop") != -1:
                farming_shop += 1

            elif line.find("from combat shop") != -1:
                combat_shop += 1

            elif line.find("from coloredblocks shop") != -1:
                colored_blocks += 1

            elif line.find("from redstone shop") != -1:
                redstone_shop += 1

            elif line.find("from ores shop") != -1:
                ores_shop_counter += 1

            elif line.find("from drops shop") != -1:
                drops_shop += 1

            elif line.find("from food shop") != -1:
                food_shop += 1

            elif line.find("from dyes shop") != -1:
                dyes_shop += 1

            elif line.find("from potions shop") != -1:
                potions_shop += 1

            elif line.find("from vip shop") != -1:
                vip_shop += 1

        total = ores_shop_counter + redstone_shop + vip_shop + drops_shop + farming_shop + \
                food_shop + blocks_shop + colored_blocks + combat_shop + dyes_shop + potions_shop

        return1 = ("\nFrom Block Shop: " + str(blocks_shop))
        return2 = ("From Farming Shop: " + str(farming_shop))
        return3 = ("From Combat Shop: " + str(combat_shop))
        return4 = ("From Colored Blocks Shop: " + str(colored_blocks))
        return5 = ("From Redstone Shop: " + str(redstone_shop))
        return6 = ("From Ores Shop: " + str(ores_shop_counter))
        return7 = ("From Drops Shop: " + str(drops_shop))
        return8 = ("From Food Shop: " + str(food_shop))
        return9 = ("From Dyes Shop: " + str(dyes_shop))
        return10 = ("From Potions Shop: " + str(potions_shop))
        return11 = ("From VIP Shop: " + str(vip_shop))
        return12 = ("\nTotal From Buys: " + str(total))


#############################################
# Money Made by IGN from Shop and SellChest #
#############################################

def ign_transactions(file, username, mode='r'):
    """Returns the amount of money earned from sales to /shop and from SellChests"""

    with open(file, mode) as text:

        total_sum_shop = 0.00
        total_sum_sellchest = 0.00

        for line in text:

            if line.find("[ShopGUIPlus]") != -1 and line.find(" sold all ") != -1 and line.find(username) != -1:
                # Manipulates string to be raw number:
                line = line[0:line.find('$')]
                line = line[line.rfind(' ') + 1:]
                line = line.replace(',', '')
                total_sum_shop += float(line)

            if line.find("[SellChest] Deposited") != -1:
                # Manipulates string to be raw number
                line = line[0:line.find(' for ')]
                line = line[line.find('$') + 1:]
                line = line.replace(',', '')
                total_sum_sellchest += float(line)

    return1 = (str(username), "sold to /shop, $" + str(round(total_sum_shop, 2)) + " in this log file")
    return2 = (str(username), "made $" + str(round(total_sum_sellchest, 2)) + " from Sell Chests in this log file")


##################################
# Stats of Possible Auto-Sellers #
##################################

def auto_sell(file, username, start_time=000000, end_time=235959, flag_mode='false', returner='none', mode='r'):
    """Returns selling statistics of a specific IGNs"""

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

    with open(file, mode) as text:
        for line in text:
            if line.find(username) != -1 and line.find("[ShopGUIPlus]") != -1 and line.find(" sold all ") != -1:
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
        if returner is 'return':
            if int(total_hours) >= 1 and differences_of_time / times_restrict <= 5 and total_money >= 10000000:
                return True

        elif flag_mode is not 'true' and returner is not 'return':
            return1 = print("\n" + username + ":")
            return2 = print("Total Money Earned: $" + str(total_money))
            return3 = print("Average Money Per Sell: $" + str(round(average_money, 2)))
            return4 = print("Time From Last Sell to First Sell: " + total_hours + " hours " + total_mins +
                            " minutes and " + total_secs + " seconds")
            return5 = print("Active Selling Time: " + str(round(minutes_selling, 2)) + " minutes")
            return6 = print("Average Time Between Sells: " + str(round(avg_time_sell, 2)) + " seconds")
            return7 = print("Amount of Breaks Selling: " + str(break_counter) + " breaks")

        return ""


###################################
# Stats of Potential Auto-Sellers #
###################################

def flag_autoseller(file, start_time=000000, end_time=235959, mode='r'):
    """Returns statistics of a potential auto-sellers"""
    igns = []  # Stores all the IGNs that need to be checked

    with open(file, mode) as text:
        for line in text:
            if line.find("[ShopGUIPlus]") != -1 and line.find(" sold all ") != -1:
                first_loc = line.find('s]')
                second_loc = line.find('sold')
                ign = line[first_loc + 3:second_loc - 1]  # Gets exact IGN

                # Only adds an IGN if it wasn't already in:
                if ign not in igns:
                    igns.append(ign)

        # Checks if each IGN passes requirements and s their stats:
        for n in range(len(igns)):
            ign_check = auto_sell(file, igns[n], returner='return')

            if ign_check:
                return1 = (auto_sell(file, igns[n]))
        return2 = ("All done!")


############################
# MobCoin Balances of IGNs #
############################

def mobcoin_balance(file, ign, mode='r'):
    """Returns the Amount of MobCoins a Player Had"""

    with open(file, mode) as text:
        for line in text:

            if line.find("[MobCoins] Balance of") != -1 and line.find(ign) != -1:
                # Finds IGN and Balance:
                index1 = line.find("of") + 3  # Begins at IGN
                index2 = line.find(".") + 3  # Ends in the hundredth place
                balance = line[index1:index2]

                # Finds Time:
                index_time1 = 1
                index_time2 = 9
                time = line[index_time1:index_time2]

                return1 = ("MobCoins of " + balance + " at " + time + " EST")


################################
# Withdrawals of Money and EXP #
################################

def withdrawals(file, type, ign='n', mode='r'):
    """Returns Withdrawals of Money and EXP as well as the grand totals"""

    total_withdrawals = 0  # Sums total money or EXP

    with open(file, mode) as text:
        for line in text:
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
                    return1 = (name + " withdrew $" + amount + " at " + time + " EST")
                    total_withdrawals += float(amount.replace(',', ''))

                elif line.find("'exp'") != -1 and type == 'exp':
                    return2 = (name + " withdrew " + amount + " of EXP at " + time + " EST")
                    total_withdrawals += float(amount.replace(',', ''))

        if type == 'money':
            return3 = ("\n$" + str(total_withdrawals) + " was withdrawn from this file")

        elif type == 'exp':
            return4 = ("\n" + str(total_withdrawals) + " EXP was withdrawn from this file")


#############################
# Deposits of Money and EXP #
#############################

def deposits(file, type, ign='n', mode='r'):
    """Returns Deposits of Money and EXP as well as the grand totals"""

    total_deposits = 0  # Sums total money or EXP

    with open(file, mode) as text:
        for line in text:
            if line.find(" valid withdrawable ") != -1 and line.find(ign) != -1:

                # Gathers IGN if global:
                if ign == "n":
                    index_name1 = line.find("draw]") + 6
                    index_name2 = line.find(" has ")
                    name = line[index_name1:index_name2]
                else:
                    name = ign

                # Gathers Amount:
                index_amount1 = line.find(" amount ") + 9
                index_amount2 = line.find(".") + 3
                amount = line[index_amount1:index_amount2].replace("'", "")

                # Gathers Time:
                time = line[1:9]

                if line.find("'arwdty-money'") != -1 and type == 'money':
                    return1 = (name + " deposited $" + amount + " at " + time + " EST")
                    total_deposits += float(amount.replace(',', ''))

                elif line.find("'arwdty-exp'") != -1 and type == 'exp':
                    return2 = (name + " deposited " + amount + " of EXP at " + time + " EST")
                    total_deposits += float(amount.replace(',', ''))

        if type == 'money':
            return3 = ("\n$" + str(total_deposits) + " was deposited from this file")

        elif type == 'exp':
            return4 = ("\n" + str(total_deposits) + " EXP was deposited from this file")


##############################
# Messages Between Player(s) #
##############################

def messages(file, from_ign, to_ign='n', mode='r'):
    """Returns all the messages sent from an IGN and the messages from conversations between 2 IGNs"""

    last_reply = ""  # Stores the last person to /msg, /m, or /tell them

    with open(file, mode) as text:
        for line in text:

            line2 = line.lower()

            if line2.find(" issued server command: /msg " + from_ign) != -1 or \
                    line2.find(" issued server command: /m " + from_ign) != -1 or \
                    line2.find(" issued server command: /tell " + from_ign) != -1 or \
                    line2.find(" issued server command: /w " + from_ign) != -1:
                # Isolates the IGN of the msg sent to:
                temp_line = line
                name = line.find("/INFO]: ") + 8
                temp_line = temp_line[name:]
                name = temp_line.find(" ")
                last_reply = temp_line[0:name]

            # Returns all the messages sent from 1 person:
            if to_ign == 'n':

                # /msg:
                if line2.find(from_ign.lower() + " issued server command: /msg ") != -1:
                    return1 = line.replace("[Server thread/INFO]: ", "")

                # /m:
                elif line2.find(from_ign.lower() + " issued server command: /m ") != -1:
                    return2 = line.replace("[Server thread/INFO]: ", "")

                # /tell:
                elif line2.find(from_ign.lower() + " issued server command: /tell ") != -1:
                    return3 = line.replace("[Server thread/INFO]: ", "")

                # /w:
                elif line2.find(from_ign.lower() + " issued server command: /w ") != -1:
                    return4 = line.replace("[Server thread/INFO]: ", "")

                # /r:
                elif line2.find(from_ign.lower() + " issued server command: /r ") != -1:
                    last_reply = fix_reply(line)
                    output = line.replace("[Server thread/INFO: ", "")
                    return5 = output.replace("issued server command: ", "replied to " + last_reply + ": ")

            # Returns all the messages between 2 people:
            elif to_ign != 'n':

                # /msg:
                if line2.find(from_ign.lower() + " issued server command: /msg " + to_ign.lower()) != -1 or \
                        line2.find(to_ign.lower() + " issued server command: /msg " + from_ign.lower()) != -1:
                    last_reply = fix_reply(line)
                    return6 = line.replace("[Server thread/INFO]: ", "")

                # /m:
                elif line2.find(from_ign.lower() + " issued server command: /m " + to_ign.lower()) != -1 or \
                        line2.find(to_ign.lower() + " issued server command: /m " + from_ign.lower()) != -1:
                    last_reply = fix_reply(line)
                    return7 = line.replace("[Server thread/INFO]: ", "")

                # /tell:
                elif line2.find(from_ign.lower() + " issued server command: /tell " + to_ign.lower()) != -1 or \
                        line2.find(to_ign.lower() + " issued server command: /tell " + from_ign.lower()) != -1:
                    last_reply = fix_reply(line)
                    return8 = line.replace("[Server thread/INFO]: ", "")

                # /w:
                elif line2.find(from_ign.lower() + " issued server command: /w " + to_ign.lower()) != -1 or \
                        line2.find(to_ign.lower() + " issued server command: /w " + from_ign.lower()) != -1:
                    last_reply = fix_reply(line)
                    return9 = line.replace("[Server thread/INFO]: ", "")

                # Person 1 /r's to Person 2:
                elif line2.find(from_ign.lower() + " issued server command: /r ") != -1 and to_ign == last_reply:
                    output = line.replace("[Server thread/INFO: ", "")
                    return10 = output.replace("issued server command: ", "replied to " + last_reply + ": ")

                # Person 2 /r's to Person 1:
                elif line2.find(to_ign.lower() + " issued server command: /r ") != -1 and from_ign == last_reply:
                    output = line.replace("[Server thread/INFO: ", "")
                    return11 = output.replace("issued server command: ", "replied to " + last_reply + ": ")


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

#print(to_purchases('/Users/tuckerbarach/Downloads/chaos_latest_77849.log'))
#auto_sell('/Users/tuckerbarach/Downloads/chaos_latest_51356.log', 'Old_Bug')
