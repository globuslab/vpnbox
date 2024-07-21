import subprocess
import json
import requests
import urllib
import secrets
from shlex import quote
import configparser
from multiprocessing import Process

config = configparser.ConfigParser()
config.read('/etc/ocserv/perm/bot.conf')

URL = "https://api.telegram.org/bot{}/".format(config.get('General', 'token'))
RIGHT_CHAT = config.getint('General', 'chat_id')
BOT_NAME = config.get('General', 'bot_name')

del config

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=10"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    #tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?chat_id={}".format(chat_id)
    myjson = {"text": text}
    requests.post(url, json = myjson, headers = headers)

def simple_send_message(text, chat_id):
    tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    get_url(url)


def send_document(doc, chat_id):
    files = {'document': open(doc, 'rb')}
    requests.post(URL + "sendDocument?chat_id={}".format(chat_id), files=files)


def send_image(doc, chat_id):
    files = {'photo': open(doc, 'rb')}
    requests.post(URL + "sendPhoto?chat_id={}".format(chat_id), files=files)


def parser(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                owner = update["message"]["from"]["username"]
                print(update)

                if chat != RIGHT_CHAT:
                    send_message("Go to chat", chat)
                    return

                text = ' '.join(text.split())
                bot_command = text.split(" ")

                if bot_command[0] == "/add" and len(bot_command) == 2:
                        username = quote(bot_command[1])
                        password = secrets.token_urlsafe(16)
                        myenv = {"USER_PASS": password}
                        myshell = '''ocpasswd -c /etc/ocserv/perm/vpn.passwd {} <<!
$USER_PASS
$USER_PASS
!'''.format(username)

                        text = subprocess.Popen(myshell, shell=True, env=myenv)

                        if text.returncode == None:
                            msg = '@{} Created user: "{}", pass: "{}"'.format(owner, username, password)
                        else:
                            msg += '''@{} Creating user: "{}" may be failed
{}
'''.format(owner, username, text)

                        send_message(msg, RIGHT_CHAT)

                elif bot_command[0] == "/list" and len(bot_command) == 1:
                    f = open("/etc/ocserv/perm/vpn.passwd", "r")
                    print(f.read())
                    msg = '''List
```
{}
```'''.format(f.read())
                    send_message(msg, RIGHT_CHAT)

                else:
                    send_message("Don't understand", RIGHT_CHAT)

def run_ocserv():
    myshell = "ocserv -f -c /etc/ocserv/ocserv.conf"
    subprocess.Popen(myshell, shell=True)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                parser(updates)

if __name__ == '__main__':
    ocserv = Process(target=run_ocserv, daemon=True)
    ocserv.start()
    ocserv.join()
    main()
