# BSY bonus - stage 5
The Stage 5 consists of only one task. You need to code in python a botnet with two parts (bot and controller) that does the following actions. 1) The bot runs on Linux, and it monitors a page in gist.github.com to download orders. 2) It executes those orders and sends back the data to gist.github.com. 3) The controller runs on Linux and can send orders to gist.github.com and receive the data back from several bots. The minimum orders are: list files in a folder, copy a file, execute a command in the bot from its operating system (e.g. /usr/bin/ps)”

## Bot implementation
Bot is a python application, that can manage only one gist page. It downloads its content every INTERVAL seconds and if there is a new command, it executes it on host OS and retures the result, error or "--empty--".
Command must start with ">". Only one-line commands are accepted. 

### Command line arguments
| short | long       |          |                            description                            |
|-------|------------|:--------:|:-----------------------------------------------------------------:|
| -g    | --git      | required | ID of a gist page                                                 |
| -u    | --user     | required | Username of the owner                                             |
| -p    | --password | required | GitHub personal access token (https://github.com/settings/tokens) |
| -f    | --file     | optional | Filename in gist, default bsy-bot.py                              |
| -i    | --interval | optional | Interval to wait in seconds, default 60                           |

## Controller implementation

Controller is a simple python script. User creates some watchers to send commands and receive results. Any controller command in gist starts with ">". Controller supports all OS specific commands(including ```cp``` and ```ls```) with their arguments. Command have to be typed exactly like in normal terminal. Only one-line commands are accepted

### Command line arguments
| short | long       |          |                            description                            |
|-------|------------|:--------:|:-----------------------------------------------------------------:|
| -i    | --interval | optional | Interval to wait in seconds, default 60                           |

### Supported commands

| command                                 |                                                                                    params                                                                                    |                      description                     |
|-----------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------:|
| bcreate <gist id> <user> <token> [file] | gist id - if of the gist page, required; user - username of the owner, required; token - personal access token, required; file - filname in gist, optional, default bsy-bot.py | Creates a new gist watcher                           |
| bdelete <id>                            | id - id of the watcher, required                                                                                                                                             | Deletes the watcher, if is not main                  |
| bswitch <id>                            | id - id of the watcher, required                                                                                                                                             | Switches the main watcher to the one with defined id |
| blist                                   |  -                                                                                                                                                                           | Lists all watchers.                                  |
| bcheck                                  |  -                                                                                                                                                                           | Checks if there are any result from the main watcher |
| Any other supported by OS command       | depends on OS                                                                                                                                                                | supported commands by OS command line                |
