import socket
import string

HOST = "irc.chat.twitch.tv"
PORT = 6667
PASS = "oauth:" # uniques_bot, put the oauth token here
IDENT = "uniques_bot"
CHANNEL = "" # channel to join

def joinRoom(s):
    readbuffer = ""
    loading = True
    st = "End of /NAMES list"
    while loading:
        readbuffer = s.recv(1024).decode("utf-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop() # removes the \n line at the end of the split list

        for line in temp:
            print(line)
            loading = loadingComplete(line)

    # sendMessage(s, "Successfully joined chat")


def loadingComplete(line):
    if("End of /NAMES list" in line):
        return False
    else:
        return True

# Opens the connection and joins the channel
def openSocket():
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", 'UTF-8'))
    s.send(bytes("NICK " + IDENT + "\r\n", 'UTF-8'))
    s.send(bytes("JOIN #" + CHANNEL + "\r\n", 'UTF-8'))
    return s
