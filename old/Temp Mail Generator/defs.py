from banner import *
from os import system
from random import choice
from httpx import get, post
from randomuser import RandomUser
system('cls')


#! Get Username
def getUsername():
    data = RandomUser()
    username = data.get_username(); return username

#! Get Domain List
def chooseDomains():
    resp = get('https://www.1secmail.com/api/v1/?action=getDomainList').json()
    print(f'''
{purple}{bold}[1] {reset}{blue}{bold}{resp[0]}{reset}
{purple}{bold}[2] {reset}{blue}{bold}{resp[1]}{reset}
{purple}{bold}[3] {reset}{blue}{bold}{resp[2]}{reset}
{purple}{bold}[4] {reset}{blue}{bold}{resp[3]}{reset}
{purple}{bold}[5] {reset}{blue}{bold}{resp[4]}{reset}
{purple}{bold}[6] {reset}{blue}{bold}{resp[5]}{reset}
{purple}{bold}[7] {reset}{blue}{bold}{resp[6]}{reset}
{purple}{bold}[8] {reset}{blue}{bold}{resp[7]}{reset}
''')
    choosedom = int(input(selectoption))
    while not choosedom in [1, 2, 3, 4, 5, 6, 7, 8]: print(checkinput); choosedom = int(input(selectoption))
    dom = resp[0] if choosedom == 1 else resp[1] if choosedom == 2 else resp[2] if choosedom == 3 else resp[3] if choosedom == 4 else resp[4] if choosedom == 5 else resp[5] if choosedom == 6 else resp[6] if choosedom == 7 else resp[7]; return dom

#! Generate Random Email
def randomMail():
    url = 'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1'
    resp = get(url).json()[0].split('@')
    username = resp[0]; domain = resp[1]; email = f'{username}@{domain}'; return username, domain, email

#! Generate Custom Email
def customEmail():
    print(custemail)
    chooseUsername = int(input(selectoption))
    if chooseUsername == 1:
        cdom = input(f'{custdom}\n> ').lower()
        if cdom == 'y': username = getUsername(); domain = chooseDomains(); email = f'{username}@{domain}'
        elif cdom == 'n': username = getUsername(); domain = choice(get('https://www.1secmail.com/api/v1/?action=getDomainList').json()); email = f"{username}@{domain}"
    elif chooseUsername == 2:
        username = input('Enter your username: ')
        cdom = input(f'{custdom}\n> ').lower()
        if cdom == 'y': domain = chooseDomains(); email = f'{username}@{domain}'
        elif cdom == 'n': domain = choice(get('https://www.1secmail.com/api/v1/?action=getDomainList').json()); email = f"{username}@{domain}"
    return username, domain, email

#! Delete Email
def delEmail(username, domain):
    payload = {'action': 'deleteMailbox', 'login': username, 'domain': domain}
    print(f'This {red}{username}@{domain}{reset} has been deleted!')
    post('https://www.1secmail.com/mailbox', data=payload)

#! Check New Message
def checkInbox(username, domain):
        resp = get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}').json()
        if len(resp) == 0:
            print(f'\n{empty}\n')
        else:
            for ID in [value for i in resp for key, value in i.items() if key=='id']:
                resp = get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={ID}').json()
                for key, value in resp.items():
                    if key == 'from': sender = value
                    elif key == 'subject': subject = value
                    elif key == 'date': date = value
                    elif key == 'textBody': content = value

                print(f'''
{blues}═════════════════════════════════════════════════════════════════╕{reset}
                      父📩 {yellow}{bold}❝ Iɴʙᴏx ❞ ㋛{reset}
{blues}══════════════════════════════════════════════════════════════════{reset}
🔥{purple} 𝕹𝖊𝖜 𝕸𝖊𝖘𝖘𝖆𝖌𝖊{reset}
   {blue}╚»{reset} {cyan}ᵴᴇᴎᴆᴇᴙ{reset} ➟  {white}{sender}{reset}
   {blue}╚»{reset} {cyan}ᴉᴆ{reset} ➟  {ID}
   {blue}╚»{reset} {cyan}ᴛᴏ{reset} ➟  {yellow}{username}@{domain}{reset}
   {blue}╚»{reset} {cyan}ᴆᴀᴛᴇ{reset} ➟  {date}
   {blue}╚»{reset} {cyan}ᵴᴜᴃᴊᴇᴄᴛ{reset} ➟  {subject}
   {blue}╚»{reset} {cyan}ᴄᴏᴎᴛᴇᴎᴛ{reset} ➟  {green}{content.strip()}{reset}
{blues}╘═════════════════════════════════════════════════════════════════{reset}
''')
