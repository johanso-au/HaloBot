# Twitch ChatBot - 2019 Johanso
#
# Modified from 'Cynigo' tutorial @:
# https://www.youtube.com/watch?v=5Kv3_V5wFgg
#
# Changes Include:
# - Settings File config.json
#       - From https://loekvandenouweland.com/content/using-json-config-files-in-python.html
#       - Guide by Loek van den Ouweland
# - Rewritten for Python 3
# - Changes to structure
# - Debug Option
#
#
#  TO DO:
# - Note list of chatters in a List, and crosscheck
#   - Check a username list for current chatter
#   - If not found, add and greet
# - Set a reset timer for when the stream goes offline and the chat goes quiet
#   - To reset the greeter for new streams.
# - Exclude list of regulars.
# - Split out "Message Action" sequence into own function
#

import socket
import json
import random
import time

DEBUG = False

with open('config.json') as configFile:
    botSettings = json.load(configFile)

# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.chat.twitch.tv"
NICK = "TwitchAccountUsername"
PASS = str(botSettings['OAUTH'])
PORT = 6667
CHANNEL = "#twitchchannelnamehere"
readbuffer = ""
MODT = False
botRun = True
userlist = []
greetings = ["hai", "Hey", "Welcome", "o hai", "hello"]

# Function for converting to UTF-8 (Required by Python 3 version of Socket)
def ConvertSend(command):
    s.sendall(command.encode('utf-8'))


# Function for sending a message
def sendMessage(message):
    ConvertSend("PRIVMSG " + CHANNEL + " :" + message + "\r\n")
    if DEBUG: print(NICK + ": " + message)


# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))

ConvertSend("PASS " + PASS + "\r\n")
ConvertSend("NICK " + NICK + "\r\n")
ConvertSend("JOIN " + CHANNEL + "\r\n")

# Main Loop - Receive, decode, parse.
while True:
    received = s.recv(1024)
    readbuffer = readbuffer + received.decode('utf-8')
    temp = readbuffer.split("\r\n")
    readbuffer = temp.pop()
    if DEBUG: print("Temp: " + str(temp))

    for line in temp:
        # Splits the given string so we can work with it better
        parts = line.split(":")
        if DEBUG: print("Parts: " + str(parts))

        # Checks whether the message is PING because its a method of Twitch to check if you're afk
        if "PING" in parts[0]:
            ConvertSend("PONG %s\r\n" % line[1])
            print("PONG")

        elif "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
            try:
                # Sets the message variable to the actual message sent
                message = parts[2]
            except:
                message = ""

            # Sets the username variable to the actual username
            usernamesplit = parts[1].split("!")
            username = usernamesplit[0]

            # Only works after twitch is done announcing stuff (MODT = Message of the day)
            if MODT:
                print(username + ": " + message + "\r\n")

                # 'On' Command.
                if username == "twitchusername" and message == "!halobotstart":
                    botRun = True
                    sendMessage("I got you, fam.")

                if botRun:

                    # You can add all your plain commands here

                    # 'Off' Command - username is a user who can control with a command.
                    if username == "twitchusername" and message == "!halobotstop":
                        botRun = False
                        sendMessage("Fine, I didn't want to do your job anyway.")

                    if username not in userlist:
                        userlist.append(username)
                        time.sleep(1)
                        sendMessage(random.choice(greetings) + " @" + username)



            for l in parts:
                if "End of /NAMES list" in l:
                    MODT = True
