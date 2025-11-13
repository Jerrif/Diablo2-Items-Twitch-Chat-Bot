import string
import time
import sqlite3
import re
from datetime import datetime

# from Read import getUser, getMessage
# from Socket import openSocket, sendMessage
from bot_init import openSocket, joinRoom, CHANNEL

s = openSocket()
joinRoom(s)

con = sqlite3.connect("d2items.db")
db = con.cursor()

# item_replacements = {'[Minimum Strength: -]':'', '[Minimum Dexterity: -]':''} # Minimal replacements, just the main annoying things
item_replacements = {'[Minimum Strength: -]':'', '[Minimum Dexterity: -]':'', '[Minimum':'[Req', 'Level Requirement':'Req Lvl', 'Damage':'Dmg', 'Chance to Cast':'CtC', 'Rest in Peace':'RiP', 'Barbarian':'Barb', 'Necromancer':'Necro', 'Sorceress':'Sorc', 'Regenerate':'Regen'}
message_replacements = {'!unique':'', '!set':'', ' ':'', "'":'', '-':'', ';':'', '\\':'', 'armour':'armor'}

readbuffer = ""

# Flag for cooldown timer
start_cooldown = False
on_cooldown = False
# Time in seconds after typing something, before being able to type again
cooldown_time = 15
start_time = time.time

def main():

    items = ["Wutface"]
    # t = Timer(10, main)
    while True:

        # if on_cooldown == True and start_cooldown == False:
        #     print("Cooldown: ", time.time - start_time)
        #     if time.time - start_time > cooldown_time:
        #         on_cooldown = False
        #         print("Off cooldown!")

        # TODO: Do this timer thing, then you're done
        # if on_cooldown == True and start_cooldown == True:
        #     start_cooldown = False
        #     start_time = time.time() # something like this I guess

        # if time.time() - t >
        readbuffer = s.recv(2048) # This was originally 1024, but it failed on large ascii messages
        temp = readbuffer.split(b"\n")
        readbuffer = temp.pop() # removes the \n line at the end of the split list

        for line in temp:
            # PING :tmi.twitch.tv
            try:
                line_decoded = line.decode("utf-8")
            except:
                line_decoded = "~~~~~~~~~~~~~~~~~~ERROR: could not decode line~~~~~~~~~~~~~~~~~~"

            # TODO: I should place this after the standard line read function
            # as this will be called much less often than other messages
            # or maybe not?
            if("PING :tmi.twitch.tv" in line_decoded):
                print("\n----------------Ping request----------------")
                print(line_decoded)
                # s.send(bytes(line.decode("utf-8").replace("PING", "PONG") + "\r\n", 'UTF-8'))
                s.send(bytes(line_decoded.replace("PING", "PONG") + "\r\n", 'UTF-8'))
                print("PONG sent back to server at: ", datetime.time(datetime.now()))
                print("----------------Ping request----------------\n")
                continue

            msg = getMsg(line_decoded)
            user = msg[0]
            message = msg[1]
            print(start_time, message)
            # print(bytes(message, 'UTF-8'))
            print('{:<25s}:{}'.format(user, message))

            # Move on if the user did not type a valid command
            if (not message.startswith("!unique")) and (not message.startswith("!set")):
                continue

            if (message == "!unique" or message == "!set") and (on_cooldown == False):
                sendMessage(s, "Usage: !unique item OR !set item, where item is a unique item name, or an item type." \
                            " Examples: !unique hatchet !unique coldkill")
                continue

            if message.startswith("!unique ") and (on_cooldown == False):
                formatted_message = multireplace(message, message_replacements).strip().lower()
                print(formatted_message)
                try:
                    data = db.execute("SELECT item_text FROM uniques WHERE search_string LIKE :f OR item_name LIKE :f", {"f":formatted_message})
                    items = db.fetchall()
                except:
                    print("Error fetching item from database")
                    items = ["Error Wutface"]
                printItems(items)
                # start_cooldown = True
                # on_cooldown = True
                # t.start()
                # for item in items:
                #     formatted_item = multireplace(item[0], item_replacements)
                #     print(formatted_item)
                #     sendMessage(s, formatted_item)
            if message.startswith("!set "):
                formatted_message = multireplace(message, message_replacements).strip().lower()
                print(formatted_message)
                try:
                    data = db.execute("SELECT item_text FROM sets WHERE search_string LIKE :f OR item_name LIKE :f", {"f":formatted_message})
                    items = db.fetchall()
                except:
                    print("Error fetching item from database")
                    items = ["Error Wutface"]
                printItems(items)
                # on_cooldown = True
                # for item in items:
                #     formatted_item = multireplace(item[0], item_replacements)
                #     print(formatted_item)
                #     sendMessage(s, formatted_item)

def printItems(items):
    for item in items:
        formatted_item = multireplace(item[0], item_replacements)
        print(formatted_item)
        sendMessage(s, formatted_item)
        time.sleep(3)


def getMsg(line):
    try:
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        # print("Prev message: ", bytes(separate[2], 'UTF-8'))
        message = separate[2].replace("\r", "")
        # print("Format message: ", bytes(message, 'UTF-8'))
    except:
        user = "~~~~~~~~~~~~~~~~~~USERNAME ERROR: "
        message = "MESSAGE ERROR~~~~~~~~~~~~~~~~~~"
    return [user, message]

# Sends a message to the channel from the bot's account
def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send(bytes(messageTemp + "\r\n", 'UTF-8'))
    print("Sent: " + messageTemp)


# TODO: Yo, I DL'd this from GitHub, check it out and try the replacements on the item_text string.
# Remember, you can't just replace "Minimum" in "Minimum Strength/Dexterity", because of "+ to minimum damage"
# https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
# https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
def multireplace(string, replacements):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :rtype: str
    """
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    substrs = sorted(replacements, key=len, reverse=True)

    # Create a big OR regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)



if __name__ == "__main__":
    main()
