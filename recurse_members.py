from datetime import datetime
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
from telethon.tl.types import ChannelParticipantsAdmins
import re
import os.path
import json
import time

# This method returns a list of Dialog, which
# get your api_id, api_hash, token
# from telegram as described above
api_id = '<YOUR>' 
api_hash = '<YOUR>'
token = '<YOUR>'
date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

message = """Hi miss/mister.


Your message !


"""
# your phone number
phone = '<BOT_ACCOUNT_PHONE>'

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('SQLiteRecrseSendSession_3', api_id, api_hash)
  
# connecting and building the session
client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():
    client.send_code_request(phone)
    # signing in the client
    client.sign_in(phone, input('Enter the code: '))
try:
    dialogs = client.get_dialogs()
    # All of these work and do the same.
    grp  = client.get_entity('https://t.me/AMA_Central')
     
    participants = client.get_participants(grp)
    admins = []
    for user in client.iter_participants(grp.id, filter=ChannelParticipantsAdmins):
        admins.append(user.id)
        print("Admin : {}, firstname: {}, lastname: {}".format(user.username, user.first_name, user.last_name))
    i = 0
    last_sent = '' 
    with open('recurse_last_sent') as f1:
        last_sent = f1.read().rstrip("\n")
    print("Last sent is {} - {}".format(last_sent,0))
    can_send = last_sent == '' 
    
    for entity in participants:
        if entity.bot==False: 
            #print(entity)
            if entity.id not in admins:
                i = i + 1 
                
                if can_send :
                    if i%8 == 0:
                        time.sleep(150)
                    else :
                        print("Sending to {}, firstname: {}, lastname: {}, entity.id: {}".format(entity.username, entity.first_name, entity.last_name,entity.id))
                        client.send_message(entity.id,message,parse_mode='html')
                        with open('recurse_last_sent', 'w') as f:
                            f.write(str(entity.id))
                        time.sleep(10)
                if str(entity.id) == last_sent:
                    can_send = True
except Exception as e:
    #there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
    print(e)
 
# disconnecting the telegram session
client.disconnect()
