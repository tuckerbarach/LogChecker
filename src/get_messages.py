import discord

member_dict = {}

def gather_messages(file_text, user1, user2):
    lines = file_text.lower().split("\n")
    last_reply = ""
    total = 0
    txt_file = open(user1 + " and " + user2 + " Messages.txt", "w+")

    member_dict = {}
    for line in lines:
        if " issued server command: " in line and (user1.lower() in line or user2.lower() in line):
            time = line[0:10]
            if line.find(" /msg ") != -1 or \
                line.find(" /message ") != -1 or \
                line.find(" /m ") != -1 or \
                line.find(" /tell ") != -1 or \
                line.find(" /w ") != -1 or \
                line.find(" /whisper ") != -1 or \
                line.find(" /r ") != -1:

                user = line[line.find("/info]:") + 8:line.find("issued server") - 1].lower()  # gets the IGN

                if " /r " not in line and user1.lower() in line and user2.lower() in line:
                    last_reply = line[line.find(" command: ") + 10:]  # gets the IGN
                    last_reply = last_reply[last_reply.find(" ") + 1:]
                    last_reply = last_reply[0:last_reply.find(" ")].lower()

                    if user in member_dict.keys():
                        member_dict.pop(user) # primed for replacement

                    if last_reply in member_dict.keys():
                        member_dict.pop(last_reply)

                    member_dict[user] = last_reply # replacement
                    member_dict[last_reply] = user

                    txt_file.write(time + " " + line[line.find("/info]:") + 8:] + "\n")
                    total += 1

                if " /r " in line and (user1.lower() in line or user2.lower() in line): # if the message is a reply:
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


