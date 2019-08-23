import json
#from test import Bunyi
import requests
import time
from datetime import date, datetime
import os
from praytimes import PrayTimes
import subprocess as terminal

TOKEN="TOKEN ANDA DISINI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
def get_url(url):
   response = requests.get(url)
   content = response.content.decode("utf-8")
   #print (content)
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

def get_news(url):
   data = get_json_from_url(url)
   print("{}".format(data))
   try:
      lat = data['results'][0]['geometry']['location']['lat']
      lng = data['results'][0]['geometry']['location']['lng']
      return (lat, lng)
   except IndexError:
      return None

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def send_document(chat_id, caption, file):
   url = URL+"sendDocument"
   files= {'document':file}
   params= {'chat_id':chat_id,'caption':caption}
   headers= {'Content-Type':'multipart/form-data'}
   resp= requests.post(url, files=files, params=params)
   return 

def send_photo(chat_id, caption, photo):
   url = URL+"sendPhoto"
   files= {'photo':photo}
   params={'chat_id':chat_id, 'caption':caption}
   headers={'Content-Type':'multipart/form-data'}
   resp= requests.post(url, files=files, params=params)
   return

def send_audio(chat_id, caption, audio):
   url = URL+"sendAudio"
   files= {'audio':audio}
   params={'chat_id':chat_id, 'caption':caption}
   headers={'Content-Type':'multipart/form-data'}
   resp= requests.post(url, files=files, params=params)
   return

def send_message(text, chat_id, pMode):
   if pMode is not None and pMode =="Markdown" or pMode == "HTML":
      url = URL+"sendMessage?text={}&chat_id={}&parse_mode={}".format(text, chat_id, pMode)
   elif pMode is not None and "json" in pMode:
      jsons={}
      pmdesplit = pMode.split("|")
      #text = (text[:600]+"..") if len(text)>600 else text
      if pmdesplit[1] is not "":
         jsons={"chat_id":chat_id, "text":text, "parse_mode":pmdesplit[1]}
      else:
         jsons={"chat_id":chat_id, "text":text}
      #print(jsons)
      response = requests.post(URL+"sendMessage", data=jsons).json()
      #print(response)
      return
   else:
      url = URL+"sendMessage?text={}&chat_id={}".format(text, chat_id)
   get_url(url)

def create_file(text):
   f = open('/media/pi/data/idbot.txt', 'a')
   f.write(str(text))
   f.close()

def read_file():
   f = open('/media/pi/data/idbot.txt', 'r+')
   text=f.read()
   f.close()
   return text

def read_source(filename):
   f = open('/home/pi/{}'.format(filename), 'r+')
   text=f.read()
   f.close()
   return text

def create_source(filename, fileExtension, text):
   f = open('/home/pi/{}.{}'.format(filename,fileExtension), 'a')
   f.write(str(text))
   f.close()
 
def read_filesuhu(namafile):
   f = open(namafile,'r+')
   text= f.read()
   f.close()
   return text

def rewrite_file(text):
   f = open('/media/pi/data/idbot.txt', 'r+')
   f.seek(0)
   f.truncate()
   f.write(str(text))
   f.close()

def tanggap(updates):
   for update in updates["result"]:
      text = update["message"]["text"]
      chat = update["message"]["chat"]["id"]
      if text.startswith("halo") :
          send_message("<i>halo juga kak</i>",chat,'HTML')
      elif text.startswith("kernelbot") :
          msg = os.uname()[1]+" "+os.uname()[2]+" "+os.uname()[4]
          send_message(msg,chat,None)
      elif text.startswith("boot") :
          p = terminal.Popen(['systemd-analyze'],stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
          
          msg,err = p.communicate()
          send_message('`'+msg.decode()+'`',chat,'Markdown')
      elif text.startswith("modaro"):
          send_message("shutting down now...",chat,None)
          text_split = text.split(' ',1)
          passwd = text_split[1]
          if 'raspberry' in passwd:
             send_message("matiin raspberry pi 3b sekarang", chat,None)
             command = 'poweroff'
             p = terminal.Popen(['sudo', '-S', command], stdin=terminal.PIPE, stderr=terminal.PIPE, universal_newlines=True)
             sudo_prompt = p.communicate(passwd + '\n')[1]
             #msg = p.returncode
             #send_message(msg, chat)
          else:
             send_message("sorry bro kamu ngga punya akses", chat,None)
      elif text.startswith("suhu"):
          # command ini disesuaikan dengan letak path file ceklamalogindantemp.sh bash script berada
          command= '/home/pi/ceklamalogindantemp.sh'.split()
          p = terminal.Popen(command,stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
          msg,error = p.communicate()
          send_message('`'+msg.decode()+'`',chat,'Markdown')
      elif text.startswith("humidity"):
          msg = "suhu dan humidity ruangan server bot: \n"
          msg += read_filesuhu('/home/pi/suhuruangan.txt')
          send_message(msg, chat,None)

      elif text.startswith("benchmark"):
          command = 'sysbench --num-threads=4 --test=cpu --cpu-max-prime=20000 --validate run'.split()
          p = terminal.Popen(command,stdout=terminal.PIPE, stderr=terminal.PIPE, stdin=terminal.PIPE)
          msg,error = p.communicate();
          print(msg.decode())
          send_message("`"+msg.decode()+"`",chat,'Markdown')
      elif text.startswith('chmod'):
          textsplit = text.split(' ', 2)
          command = 'chmod {} /home/pi/{}'.format(textsplit[1], textsplit[2]).split()
          p = terminal.Popen(command, stdout=terminal.PIPE, stderr=terminal.PIPE, stdin=terminal.PIPE)
          msg,err = p.communicate()
          if err.decode() is not "":
             send_message('galat maaf bray belajar chmod dulu sono', chat,None)
          else:
             if msg.decode() is not "":
                send_message(msg, chat,None)
             else:
                send_message('sukses chmod', chat,None)
      elif text.startswith("sholat"):
          textsplit = text.split(' ',1)
          kota = textsplit[1];
          urlkota = "https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty"
          latdanlng = get_news(urlkota)
          if latdanlng is None:
             send_message("latlon belum ketemu",chat,None)
             return
          j = PrayTimes()
          times = j.getTimes(date.today(), latdanlng , 7)
          string_reply = "Jadwal Sholat untuk kota {} dalam wib sekarang jam {} wib \n".format(kota, datetime.now().time())
          for u in ['Imsak','Fajr','Sunrise','Dhuhr','Asr','Maghrib','Isha']:
              string_reply += (u + ': '+times[u.lower()])+'\n'
          send_message('<b>'+string_reply+'</b>', chat,'HTML') 
      elif text.startswith("cocok"):
          textsplit = text.split(' ',2)
          unitext = textsplit[1]+textsplit[2]
          lentext = len(unitext)
          alentext = lentext + 20
          kalitext = lentext + alentext
          string_replay = "kecocokan {} dan {} sekitar {}%".format(textsplit[1], textsplit[2], kalitext)
          send_message(string_replay, chat,None)
      
      elif text.startswith("write_code"):
          textsplit = text.split(' ', 3)
          if os.path.isfile("/home/pi/"+textsplit[1]+"."+textsplit[2]):
             send_message("file telah dibuat", chat, None)
          else:
             send_message('creating source code {}.{}'.format(textsplit[1], textsplit[2]), chat,None)
             create_source(textsplit[1], textsplit[2], textsplit[3])
             send_document(chat,"file yang terbentuk", open('{}.{}'.format(textsplit[1],textsplit[2]),'rb'))
      elif text.startswith("compile_code"):
          textsplit = text.split(' ', 2)
          if os.path.isfile('/home/pi/{}'.format(textsplit[1])):
             if textsplit[1].endswith('go'):
                command = 'go build /home/pi/{}'.format(textsplit[1]).split()
             elif textsplit[1].endswith('ts'):
                command ='tsc /home/pi/{}'.format(textsplit[1]).split()
             else: 
                command = 'gcc -std=gnu99 -o {} /home/pi/{}'.format(textsplit[2], textsplit[1]).split()
             p = terminal.Popen(command,stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
             msg,error = p.communicate()
             #print "{} and {}".format(msg, error)
             if error.decode() is not "":
                print("{}".format(error))
                if "error" in  error.decode():
                   send_message("galat waktu ngompile %s"%(error.decode()), chat,None)
                else:
                   send_message("sukses %s"%(error.decode()), chat, None)
             else:
                send_message('sukses compile', chat,None)
          else:
             send_message('source code tidak ditemukan', chat,None)

      elif text.startswith("read_code"):
          textsplit = text.split(' ')
          if os.path.isfile('/home/pi/{}'.format(textsplit[1])):
             msg= "your source code is:\n`"
             msg += read_source(textsplit[1])
             msg += "`"
             print(msg)
             send_message(msg.encode(), chat, "json|Markdown");
          else:
             send_message('source code dengan nama file {} belum dibuat'.format(textsplit[1]), chat,None)

      elif text.startswith("run_code"):
          textsplit = text.split(' ', 1)
          if os.path.isfile('/home/pi/{}'.format(textsplit[1])):
             if textsplit[1].endswith('py'):
                command = 'python /home/pi/{}'.format(textsplit[1]).split()
             elif textsplit[1].endswith('go'):
                command = 'go run /home/pi/{}'.format(textsplit[1]).split()
             elif textsplit[1].endswith('sh'):
                command = 'sh /home/pi/{}'.format(textsplit[1]).split()
             elif textsplit[1].endswith('js'):
                command = 'node /home/pi/{}'.format(textsplit[1]).split()
             else:
                command = '/home/pi/{}'.format(textsplit[1]).split()
             p = terminal.Popen(command,stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
             msg,error = p.communicate()
             psn=""
             if error.decode() is not "":
                psn = "galat `"
                psn += error.decode()
                psn += "`"
             else:
                psn = "`"
                psn += msg.decode()
                psn += "`"
             send_message(psn, chat ,'Markdown')
          else:
             send_message("program {} tidak ditemukan".format(textsplit[1]), chat,None) 

      elif text.startswith("play"):
          send_message('<b><i> putar lagu free software song </i></b>',chat, 'HTML')
          command = 'mpv --no-video /media/pi/data/Lagu-Lagu/freeSWSong.ogg'.split()
          p=terminal.Popen(command,stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
          p.communicate()
      elif text.startswith("run_gpio"):
          textsplit = text.split(' ', 1)
          if os.path.isfile('/home/pi/{}'.format(textsplit[1])):
             if textsplit[1].endswith('py'):
                command = 'sudo python /home/pi/{}'.format(textsplit[1]).split()
             elif textsplit[1].endswith('go'):
                command = 'sudo go run /home/pi/{}'.format(textsplit[1]).split()
             elif textsplit[1].endswith('sh'):
                command = 'sudo sh /home/pi/{}'.format(textsplit[1]).split()
             else:
                command = 'sudo /home/pi/{}'.format(textsplit[1]).split()
             p = terminal.Popen(command,stdout=terminal.PIPE,stderr=terminal.PIPE,stdin=terminal.PIPE)
             msg,error = p.communicate()
             psn=""
             if error.decode('utf-8') is not "":
                psn = "galat `"
                psn += error.decode('utf-8')
                psn += "`"
             else:
                psn = "`"
                psn += msg.decode('utf-8')
                psn += "`"
             send_message(psn, chat,'Markdown')
          else:
             send_message('program {} tidak ditemukan'.format(textsplit[1]), chat,None) 
      elif text.startswith("wakeup"):
          textsplit= text.split(' ')
          bunyi = Bunyi(textsplit[1])
          send_message('<b>set alarm jam {}</b>'.format(bunyi.read_file()),chat,'HTML')
      elif text.startswith("/start"):
          msg="""
               silahkan pilih command yang tersedia untuk umum:
               1. halo untuk menyapa bot
               2. sholat <spasi> <nama kota> untuk informasi waktu sholat
               3. aku untuk informasi bot berjalan di system apa hehe"""
          send_message("`"+msg+"`",chat,"Markdown")
      elif text.startswith("log"):
          command = "cat /var/log/lastlog".split()
          p = terminal.Popen(command, stdout=terminal.PIPE, stderr=terminal.PIPE, stdin=terminal.PIPE)
          msg,err = p.communicate()
          if err.decode('utf-8') is not "":
             mer= "galat `"
             mer += err.decode('utf-8')
             mer += "`"
             print (chat)
             send_message(mer, chat, "Markdown")
          else:
             psn ="`"
             psn += msg.decode('utf-8')
             psn += "`"
             print(chat)
             print(psn)
             send_message(psn, chat, "json|Markdown")
             #send_message(psn, chat, "Markdown")
      elif text.lower().startswith("kirimdoc"):
          textsplit = text.split(' ')
          file = textsplit[1]
          if os.path.isfile('{}'.format(file)):
             caption= "mengirim berkas {}".format(file)
             send_document(chat, caption, open(file, 'rb'))
          else:
             send_message("maaf berkas tidak tersedia", chat, None)
      elif text.lower().startswith("kirimaudio"):
          textsplit= text.split(" ")
          file = textsplit[1]
          if os.path.isfile('/media/pi/data/Lagu-Lagu/{}'.format(file)):
             caption= "mengirim audio {}".format(file)
             send_audio(chat, caption, open('/media/pi/data/Lagu-Lagu/{}'.format(file), 'rb'))
          else:
             send_message("maaf berkas audio {} tidak ditemukan.".format(file), chat, None)
      elif text.lower().startswith("kirimphoto"):
          textsplit = text.split(' ')
          file = textsplit[1]
          if os.path.isfile("/media/pi/data/{}".format(file)):
             caption = "mengirim berkas gambar {}".format(file)
             send_photo(chat, caption, open('/media/pi/data/{}'.format(file), 'rb'))
          else:
             send_message("maaf berkas gambar {} tidak ditemukan".format(file), chat, None)

def main():
    last_update_id = None
    while True:
        if os.path.isfile('/media/pi/data/idbot.txt'):
           last_update_id = int(read_file()) 
        updates = get_updates(last_update_id)
        #print (updates['result'])
        leng = len(updates['result'])
        if leng > 0:
           last_update_id = get_last_update_id(updates) + 1
           if not os.path.isfile('/media/pi/data/idbot.txt'):
              create_file(last_update_id)
           else:
              rewrite_file(last_update_id)
           tanggap(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
