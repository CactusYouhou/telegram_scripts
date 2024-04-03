from datetime import datetime
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import re
import os.path
import json

last_binance_listed = '' 
last_binance_readed = '' 
last_kcs_listed = '' 
last_kcs_readed = ''

with open('listing_kucoin') as f1:
    kcs_lines = f1.read()
    kcs_json = json.loads(kcs_lines)
    last_listing = kcs_json['items'][0]['title']
    last_kcs_readed = last_listing 

with open('listing_binance') as f:
    lines = f.read()
    m = re.search('Binance Will List (\w+)\s*\(', lines)
    last_binance_readed = m.group(1)

if (os.path.isfile('last_binance_listed')):
    with open('last_binance_listed') as f:
        last_binance_listed = f.read()
else :
    last_binance_listed = last_binance_readed

if (os.path.isfile('last_kcs_listed')):
    with open('last_kcs_listed') as f:
        last_kcs_listed = f.read() 
else :
    last_kcs_listed = last_kcs_readed


with open('last_binance_listed', 'w') as f:
    f.write(last_binance_readed)

with open ('last_kcs_listed','w') as f:
    f.write(last_kcs_readed)

send_binance_message = last_binance_listed != last_binance_readed 

send_kcs_message = last_kcs_listed != last_kcs_readed

send_message = send_binance_message  or send_kcs_message

if (send_message):

    # get your api_id, api_hash, token
    # from telegram as described above
    api_id = '<YOUR_APP_ID>'

    api_hash = '<YOUR_API_HASH>'
    token = '<YOUR_TOKEN>'
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    binance_message = "{} - Binance list {}".format(date,last_binance_readed)
    kcs_message = "{} - {}".format(date,last_kcs_readed)

    # your phone number
    phone = '<PHONE_NUMBER_OF_THE_BOT_ACCOUNT>'
  
    # creating a telegram session and assigning
    # it to a variable client
    client = TelegramClient('SQLiteSession', api_id, api_hash)
      
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
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
        receiver = InputPeerUser('user_id', 'user_hash')
        print("Sending message") 
        # sending message using telegram client
        telegram_user_id='telegram_user_id'
        if (send_binance_message):
            client.send_message(telegram_user_id,binance_message, parse_mode='html')
        if (send_kcs_message):
            client.send_message(telegram_user_id,kcs_message,parse_mode='html')
    except Exception as e:
     
        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e)
 
    # disconnecting the telegram session
    client.disconnect()
