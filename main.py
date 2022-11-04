import telethon
import asyncio
import os, sys
import re
import requests
from telethon import TelegramClient, events
from random_address import real_random_address
import names
from datetime import datetime
import random


from defs import getUrl, getcards, phone
API_ID =  11849455
API_HASH = '0956032efc5694f60156fe65f9c19764'
SEND_CHAT = '@scrappertb'

client = TelegramClient('session', API_ID, API_HASH)
ccs = []

chats  = [
    # '@fullcuentasgratis','
    '@LalaScrap',
    '@ScrapperLost',
    '@DollyBinsChat',
    '@secretgroup01',
    '@CCsdiarioss',
    '@savagegroupoficial',
    '@RemChatChk',
    '@accerroreschecker',
    '@LigthStormChat'   
]

with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()


for x in temp_cards:
    car = getcards(x)
    if car:
        ccs.append(car[0])
    else:
        continue

@client.on(events.NewMessage(chats=chats, func = lambda x: getattr(x, 'text')))
async def my_event_handler(m):
    if m.reply_markup:
        text = m.reply_markup.stringify()
        urls = getUrl(text)
        if not urls:
            return
        text = requests.get(urls[0]).text
    else:
        text = m.text
    cards = getcards(text)
    if not cards:
        return
    cc,mes,ano,cvv = cards
    if cc in ccs:
        return
    ccs.append(cc)
    bin = requests.get(f'https://adyen-enc-and-bin-info.herokuapp.com/bin/{cc[:6]}')
    if not bin:
        return
    bin_json =  bin.json()
    addr = real_random_address()
    fullinfo = f"{cc}|{mes}|{ano}|{cvv}|{names.get_full_name()}|{addr['address1']}|{addr['city']}|{addr['state']}|{addr['postalCode']}|{phone()}|dob: {datetime.strftime(datetime(random.randint(1960, 2005), random.randint(1, 12),random.randint(1, 28), ), '%Y-%m-%d')}|United States Of America"
    text = f"""
╔═══════════════════════╗
╟ ● **𝑺𝒄𝒓𝒂𝒑𝒑𝒆𝒓 𝑪𝑪 「𝚃𝙱」** 
╟═══════════════════════╝
╟ [🝂] __𝗖𝗮𝗿𝗱 - ↯__:
╟ ╙ `{cc}|{mes}|{ano}|{cvv}`
╟ [🝂] _𝗜𝗻𝗳𝗼 - ↯__:
╟ ╙ {bin_json['vendor']} - {bin_json['type']} - {bin_json['level']}
╟ ╙ {bin_json['bank']}
╟ ╙ {bin_json['country_iso']} - {bin_json['flag']}
╟ [🝂] __𝙊𝙬𝙣𝙚𝙧𝙨 - ↯__: @SuperHaHa1 & @XerozSploitTae__
╚═══════════════════════╝
"""    
    print(f'{cc}|{mes}|{ano}|{cvv}')
    with open('cards.txt', 'a') as w:
        w.write(fullinfo + '\n')
    await client.send_message(SEND_CHAT, text, link_preview = False)




@client.on(events.NewMessage(outgoing = True, pattern = re.compile(r'[./!]extrap( (.*))')))
async def my_event_handler(m):
    text = m.pattern_match.group(1).strip()
    with open('cards.txt', 'r') as r:
        cards = r.read().splitlines() # list of cards
    if not cards:
        return await m.reply("Not Found")
    r = re.compile(f"{text}*.")
    if not r:
        return await m.reply("Not Found")
    newlist = list(filter(r.match, cards)) # Read Note below
    if not newlist:
        return await m.reply("Not Found")
    if len(newlist) == 0:
        return await m.reply("0 Cards found")
    cards = "\n".join(newlist)
    return await m.reply(cards)


@client.on(events.NewMessage(outgoing = True, pattern = re.compile(r'.lives')))
async def my_event_handler(m):
    # emt = await client.get_entity(1582775844)
    # print(telethon.utils.get_input_channel(emt))
    # print(telethon.utils.resolve_id(emt))
    await m.reply(file = 'cards.txt')



client.start()
client.run_until_disconnected()
