import json
import requests
import time
import os
import subprocess as terminal

TOKEN="TOKENMU_DISINI_AMBIL_DARI_BOTFATHER"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
def get_url(url):
   response = requests.get(url)
   content = response.content.decode("utf8")
   return content

def get_json_from_url(url):
   content = get_url(url)
   js = json.loads(content)
   return js

def get_updates(offset=None):
   url = URL+"getUpdates"
   if offset :
      url += "?offset={}".format(offset)
   js = get_json_from_url(url)
   return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
   url = URL+"sendMessage?text={}&chat_id={}".format(text, chat_id)
   get_url(url)

def create_file(text):
   f = open('/media/arba/data/mybot/idbot.txt', 'a')
   f.write(str(text))
   f.close()

def read_file():
   f = open('/media/arba/data/mybot/idbot.txt', 'r+')
   text=f.read()
   f.close()
   return text

def rewrite_file(text):
   f = open('/media/arba/data/mybot/idbot.txt', 'r+')
   f.seek(0)
   f.truncate()
   f.write(str(text))
   f.close()

def tanggap(updates):
   for update in updates["result"]:
      text = update["message"]["text"]
      chat = update["message"]["chat"]["id"]
      if "halo" in text :
          send_message("halo juga kak",chat)
      elif "aku" in text :
          msg = os.uname()[1]+" "+os.uname()[2]+" "+os.uname()[4]
          send_message(msg,chat)
      elif "boot" in text :
          p = terminal.Popen(['systemd-analyze'],stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
          
          msg,err = p.communicate()
          send_message(msg,chat)
      elif "shutdown" in text:
          send_message("shutting down now...",chat)
          text_split = text.split(' ',1)
          passwd = text_split[1]
          command = 'poweroff'
          p = terminal.Popen(['sudo', '-S', command], stdin=terminal.PIPE, stderr=terminal.PIPE, universal_newlines=True)
          sudo_prompt = p.communicate(passwd + '\n')[1]
      elif "suhu" in text:
          # command ini disesuaikan dengan letak path file ceklamalogindantemp.sh bash script berada
          command= '/home/arba/ceklamalogindantemp.sh'
          p = terminal.Popen([command],stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
          msg,error = p.communicate()
          send_message(msg,chat)
      elif "benchmark" in text:
          command = 'sysbench --num-thread=4 --test=cpu --cpu-max-prime=20000 --validate run'.split()
          p = terminal.Popen([command],stdout=terminal.PIPE, stderr=terminal.PI$
          msg,error = p.communicate();
          send_message(msg,chat)
      else :
          send_message("echo "+text,chat)
       

def main():
    last_update_id = None
    while True:
        if os.path.isfile('/media/arba/data/mybot/idbot.txt'):
           last_update_id = int(read_file()) 
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
           last_update_id = get_last_update_id(updates) + 1
           if not os.path.isfile('/media/arba/data/mybot/idbot.txt'):
              create_file(last_update_id)
           else:
              rewrite_file(last_update_id)
           tanggap(updates)
                       
        time.sleep(0.5)

if __name__ == '__main__':
    main()