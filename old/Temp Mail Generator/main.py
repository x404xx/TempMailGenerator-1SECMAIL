from defs import *
from banner import *
from os import remove
from re import findall


def main():
    print(generator)
    sel = int(input(selectoption))
    while not sel in [1, 2, 3, 4, 5]: print(checkinput); sel = int(input(selectoption))
    if sel == 1: username, domain, email = randomMail(); print(f'Your Email: {yellow}{email}{reset}'); checkInbox(username, domain); open('AllEmail.txt', 'a').write(f'{email}\n')
    elif sel == 2: username, domain, email = customEmail(); print(f'Your Email: {yellow}{email}{reset}'); checkInbox(username, domain); open('AllEmail.txt', 'a').write(f'{email}\n')
    elif sel == 3: checkInbox(input('Your username: '), input('Your domain: '))
    elif sel == 4:
        print(deletemail)
        manu = int(input(selectoption))
        while not manu in [1, 2]: print(checkinput); manu = int(input(selectoption))
        if manu == 1: delEmail(input('Your username: '), input('Your domain: '))
        else:
            for username, domain in findall(r'(\w+)@(\w+.*)', open('AllEmail.txt').read().strip()): delEmail(username, domain)
            remove('AllEmail.txt'); print(f'\n{remtxt}\n')
    else: exit('\nBye..\n')


if __name__ == '__main__':
    print(logo)
    main()
