import os
import sys
import getopt
import requests
import base64
import json
import  time

API = "https://api.github.com/gists"
FILE = "bsy-bot.py"
INTERVAL = 60

bots = {}
counter = 0;
main_bot = -1;

def write_to_file(file_content):
    global counter, main_bot
    if (main_bot == -1):
        print("Choose the main watcher!")
        return
    path = API + "/"+main_bot["gist"]
    data = {"files": {main_bot["file"] : {"content": file_content}}}
    r = requests.patch(path, headers=main_bot["headers"], data=json.dumps(data))
    if (r.status_code != 200):
        print("error occured: ")
        print(r.json())

def read_file():
    global counter, main_bot
    if (main_bot == -1):
        print("Choose the main watcher!")
        return
    path = API + "/"+main_bot["gist"]
    r = requests.get(path, headers=main_bot["headers"])
    if (r.status_code != 200):
        print("error occured: ")
        print(r.json())
        return True
    data = r.json()
    files = data["files"]
    file = files[main_bot["file"]]
    try:
        content = file["content"];
        if (file["truncated"]):
            print("Cannot process truncated file, file is too big. Delete content")
            return True
        lines = content.splitlines();
        returnedLines = []
        for l in reversed(lines):
            if (l.startswith(">")):
                break
            returnedLines.insert(0, l);
                
        if (len(returnedLines) == 0):
            answer = input("No changes detected. Do you want to wait another " + str(INTERVAL) + "seconds? (y/n): ")
            while (answer not in ['y', 'n']):
                answer = input("Please, type 'y' or 'n': ")
            return answer == 'n'
        else: 
            for l in returnedLines:
                print(l)
            return True
    except KeyError:
        print("error reading file with filename " + main_bot["file"])

def create(gist, user, token, file):
    global counter, main_bot
    if (not file):
        file = FILE
    myStr = "%s:%s" % (user, token);
    headers ={'Accept':'application/vnd.github.v3+json', "Authorization" : "Basic " + base64.urlsafe_b64encode(myStr.encode()).decode()}
    counter+=1
    bots[str(counter)] = {"id":str(counter), "gist": gist, "headers": headers, "file": file}
    if (main_bot == -1):
        main_bot = bots[str(counter)]
    return counter;

def delete(id):
    global counter, main_bot
    try:
        if (main_bot != -1 and main_bot["id"] == id):
            print("Cannot delete current watcher with id "+ id+". Switch to another bot to delete the current one")
            return
        del bots[id]
    except:
        print("Cannot delete watcher with id "+ id)

def blist():
    global counter, main_bot
    print("ID\tGIST ID\t\tFILE\n")
    print("-----------------------\n")
    for key in bots:
        if (main_bot != -1 and main_bot["id"] == key):
            new_key = "* "+ key
        else:
            new_key = key
        print(new_key + "\t" + bots[key]["gist"] + "\t" + bots[key]["file"] + "\n")

def switch(id):
    global counter, main_bot
    try:
        main_bot = bots[id] #check if exists
    except KeyError:
        print("Watcher with id " + id + " does not exist. Try blist command to see all available bots or bcreate to create a new one")



print("Starting contoller .....")

opts, args = getopt.getopt(sys.argv[1:], "i:", ["interval="]);
for opt, arg in opts:
    if (opt in ['-i', '--interval']):
        INTERVAL = int(arg)
    else:
        print("warn: Cannot recognize option "+ opt)

print("""
Commands:
bcreate <gist id> <user> <token> [file]- creates a new page watcher 
bdelete <id> - deletes page watcher
bswitch <id> - switches to another page watcher
blist - list of page watchers
bcheck - check if there is an output from a watcher
""")



while True:
    command = input(">");
    if (command.startswith("bcreate")):
        args = command.split()[1:]
        if (len(args) == 3):
            id = create(args[0], args[1], args[2], FILE)
            print("Created new watcher with id " + str(id))
            print("Main watcher is " + main_bot["id"])
        elif(len(args) == 4):
            id = create(args[0], args[1], args[2], args[3])
            print("Created new watcher with id " + str(id))
            print("Main watcher is " + main_bot["id"])
        else:
            print("Invalid arguments")
    elif(command.startswith("bdelete")):
        args = command.split()[1:]
        if (len(args) == 1):
            delete(args[0])
        else:
            print("Invalid arguments")
    elif(command.startswith("bswitch")):
        args = command.split()[1:]
        if (len(args) == 1):
            switch(args[0])
        else:
            print("Invalid arguments")
    elif(command.startswith("blist")):
        blist()
    elif(command.startswith("bcheck")):
        while True:
            read = read_file()
            if (not read):
                print("WAITING...")
                time.sleep(INTERVAL)
            else:
                break
    else:
        write_to_file(">" + command)
        while True:
            read = read_file()
            if (not read):
                print("WAITING...")
                time.sleep(INTERVAL)
            else:
                break
    