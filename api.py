import json
import os
import random
import re
import sys
import time

import httpx
import inquirer


class EmailGenerator:
    FILENAME = 'email.json'

    def __init__(self):
        self.client = httpx.Client(timeout=random.uniform(10, 15))

    def __del__(self):
        self.client.close()
        print('\nSession has been closed!\n')

    @property
    def __domain_list(self):
        url = 'https://www.1secmail.com/api/v1/?action=getDomainList'
        response = self.client.get(url)
        return response.json()

    def __user_info(self):
        url = 'https://randomuser.me/api/?nat=US&password=upper,lower,number,10-16'
        response = self.client.get(url)
        response_json = response.json()

        result = response_json['results'][0]
        user = result['name']
        login = result['login']

        return {
            'username': login['username'],
            'password': login['password'],
            'first_name': user['first'],
            'last_name': user['last']
        }

    def get_names(self):
        user_info = self.__user_info()
        return user_info['first_name'], user_info['last_name']

    def get_password(self):
        user_info = self.__user_info()
        return user_info['password']

    def __get_domain(self):
        questions = [
            inquirer.List('domain', message="Which domain do you want?", choices=self.__domain_list)
        ]
        answers = inquirer.prompt(questions)
        return answers['domain']

    def random_email(self):
        username = self.__user_info()['username']
        domain = random.choice(self.__domain_list)
        return username, domain

    def custom_email(self):
        username = input('Your desire username: ')
        domain = self.__get_domain()
        return username, domain

    def delete_mailbox(self, username, domain):
        url = 'https://www.1secmail.com/mailbox'
        data = {'action': 'deleteMailbox', 'login': username, 'domain': domain}
        response = self.client.delete(url, data=data)
        if response.status_code == 200:
            return True
        return False

    def save_email(self, email):
        data = {}

        if os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'r') as file:
                data = json.load(file)

        data.setdefault('email', []).append(email)

        with open(self.FILENAME, 'w') as file:
            json.dump(data, file, indent=4)

    def __check_inbox(self, username, domain):
        url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}'
        response = self.client.get(url)
        return response.json()

    def __get_id(self, username, domain):
        inbox = self.__check_inbox(username, domain)
        if inbox:
            latest_id = max(inbox, key=lambda x: x['id'])['id']
            return latest_id
        else:
            print('No messages found in the inbox!')
            return None

    def get_message(self, username, domain):
        retries = 0
        while retries < 3:
            self.__waiting_time()
            message_id = self.__get_id(username, domain)

            if message_id is None:
                retries += 1
                continue

            read_message = self.__read_message(username, domain, message_id)

            return {
                'id': message_id,
                'sender': read_message['sender'],
                'subject': read_message['subject'],
                'date': read_message['date'],
                'message': read_message['message']
            }

        print('Maximum number of retries exceeded!')
        sys.exit(0)

    def __waiting_time(self):
        for i in range(5):
            print(f'Refreshing inbox in {(5 - i)} seconds', end='\r')
            time.sleep(1)
            print(end='\r\033[K')

    def __read_message(self, username, domain, message_id):
        url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}'
        response = self.client.get(url)
        response_json = response.json()

        return {
            'sender': response_json.get('from'),
            'subject': response_json.get('subject'),
            'date': response_json.get('date'),
            'message': response_json.get('textBody') or response_json.get('body') or response_json.get('htmlBody')
        }

    def verification_code(self, pattern, message):
        veri_code = re.search(pattern, message)
        return veri_code[0] if veri_code else None

    def get_user_input(self, prompt, choices):
        while True:
            user_input = input(prompt).lower()
            if user_input in choices:
                return user_input
            print('Invalid input! Please try again.')