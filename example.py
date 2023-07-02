import json
import os
import sys

from user_agent import generate_user_agent as ua

from api import EmailGenerator
from color import Colors


class TestRegistration(EmailGenerator):

    def __init__(self):
        super().__init__()
        self.client.headers.update({
            'User-Agent': str(ua()),
            'content-type': 'application/json',
        })
        print(f"UA: {Colors.LBLUE}{self.client.headers['User-Agent']}{Colors.END}")

    def __sign_up(self, email, first_name, last_name):
        json_data = {
            'operationName': 'signup_init',
            'variables': {
                'appv': {
                    'release': 'web',
                    'version': 'beta',
                    'env': 'production',
                },
                'email': email,
                'firstname': first_name,
                'lastname': last_name,
            },
            'query': 'mutation signup_init($email: String!, $firstname: String!, $lastname: String!, $appv: appvInput!) {\n  signup_init(email: $email, firstname: $firstname, lastname: $lastname, appv: $appv) {\n    result\n    message\n    __typename\n  }\n}\n',
        }
        try:
            response = self.client.post('https://api.testmail.app/api/admin/graphql', json=json_data)
        except Exception as exc:
            print(str(exc))

        response_json = response.json()
        result = response_json['data']['signup_init']

        if result['result'] == 'success':
            print(f'{Colors.BGREEN}Signup succcessfully!{Colors.END}')
        elif result['result'] == 'fail' and 'Already registered' in result['message']:
            print(f'{Colors.RED}Already registered! {Colors.WHITE}Try with another email{Colors.END}')
            sys.exit(0)
        else:
            print(f'{Colors.RED}Signup failed!{Colors.END}')
            sys.exit(0)

    def __complete_signup(self, email, otp):
        json_data = {
            'operationName': 'signup_complete',
            'variables': {
                'appv': {
                    'release': 'web',
                    'version': 'beta',
                    'env': 'production',
                },
                'email': email,
                'code': otp,
            },
            'query': 'mutation signup_complete($email: String!, $code: String!, $appv: appvInput!) {\n  signup_complete(email: $email, code: $code, appv: $appv) {\n    result\n    message\n    signed\n    __typename\n  }\n}\n',
        }

        response = self.client.post('https://api.testmail.app/api/admin/graphql', json=json_data)
        response_json = response.json()
        signup_complete = response_json['data']['signup_complete']
        result = signup_complete['result']
        if result == 'success':
            print(f'{Colors.BGREEN}Signup Completed with an OTP!{Colors.END}')
        token = signup_complete['signed']
        return token

    def __verify_token(self, token):
        params = {'key': 'AIzaSyAfjg4uG2byJSqbw9bqgLqMTc8sBORBwM8'}
        json_data = {
            'token': token,
            'returnSecureToken': True,
        }

        response = self.client.post(
            'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken',
            params=params,
            json=json_data,
        )
        response_json = response.json()
        id_token = response_json['idToken']
        return id_token

    def __verify_email(self, id_token):
        params = {'key': 'AIzaSyAfjg4uG2byJSqbw9bqgLqMTc8sBORBwM8'}
        json_data = {
            'idToken': id_token,
        }

        response = self.client.post(
            'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo',
            params=params,
            json=json_data,
        )
        response_json = response.json()
        users = response_json['users'][0]
        email_verified = users['emailVerified']
        if email_verified == True:
            print(f'{Colors.BGREEN}Email has been verified successfully!{Colors.END}')

    def __get_result_info(self, id_token):
        self.client.headers.update({'authorization': f'Bearer {id_token}'})
        json_data = {
            'operationName': 'everything',
            'variables': {
                'appv': {
                    'release': 'web',
                    'version': 'beta',
                    'env': 'production',
                },
            },
            'query': 'query everything($appv: appvInput!) {\n  everything(appv: $appv) {\n    user {\n      uid\n      t\n      firstname\n      lastname\n      primaryemail\n      viewbox\n      promoemails\n      invites {\n        id\n        t\n        oid\n        orgname\n        invitee\n        role\n        inviter {\n          email\n          firstname\n          lastname\n          __typename\n        }\n        accepted\n        revoked\n        rejected\n        __typename\n      }\n      hmac\n      __typename\n    }\n    orgs {\n      oid\n      t\n      name\n      plan\n      limits {\n        apikey_create\n        namespace_create\n        namespace_custom\n        retention\n        __typename\n      }\n      namespaces {\n        t\n        namespace\n        enabled\n        usage {\n          year\n          month\n          use\n          __typename\n        }\n        __typename\n      }\n      apikeys {\n        t\n        apikey\n        enabled\n        namespaces\n        usage {\n          year\n          month\n          use\n          __typename\n        }\n        __typename\n      }\n      members {\n        mid\n        uid\n        t\n        role\n        firstname\n        lastname\n        primaryemail\n        viewbox\n        __typename\n      }\n      invites {\n        id\n        t\n        oid\n        orgname\n        invitee\n        role\n        inviter {\n          email\n          firstname\n          lastname\n          __typename\n        }\n        accepted\n        revoked\n        rejected\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        response = self.client.post('https://api.testmail.app/api/admin/graphql', json=json_data)
        response_json = response.json()
        orgs = response_json['data']['everything']['orgs'][0]
        apikeys = orgs['apikeys'][0]
        usage = apikeys['usage'][0]

        return {
            'created': f'{usage["month"]}|{usage["year"]}',
            'role': orgs['members'][0]['role'],
            'apikey': apikeys['apikey'],
            'apikey_usage': usage['use'],
            'plan': orgs['plan']
        }

    def start_register(self):
        custom_email = self.get_user_input('Do you want to custom domain? (y/n): ', ['y', 'n'])
        username, domain = '', ''
        if custom_email == 'y':
            username, domain = self.custom_email()
        elif custom_email == 'n':
            username, domain = self.random_email()

        email = f'{username}@{domain}'
        print(f'Your email {Colors.GREEN}{email}{Colors.END} has been created successfully!')

        first_name, last_name = self.get_names()
        print(f'Name: {Colors.BYELLOW}{first_name} {last_name}{Colors.END}')

        save_email = self.get_user_input('Do you want to save the email? (y/n): ', ['y', 'n'])
        if save_email == 'y':
            self.save_email(email)
            print(f'Your email {Colors.GREEN}{email}{Colors.END} has been saved successfully in {Colors.LPURPLE}{self.FILENAME}{Colors.END}!')
        else:
            print(f'{Colors.RED}The save has been skipped!{Colors.END}')

        self.__sign_up(email, first_name, last_name)
        message_info = self.get_message(username, domain)

        sender = message_info['sender']
        print(f'You have received a message from {Colors.WHITE}{sender}{Colors.END}')

        message_id = message_info['id']
        print(f'Message ID: {Colors.LPURPLE}{message_id}{Colors.END}')

        #! Please edit the regex pattern suitable for the confirmation code that is received from a website.
        message = message_info['message']
        pattern = r'\b[A-Z0-9]+\b' #! This pattern will capture the code for example (ADJBS, CYSRA6L, 753234)
        otp = self.verification_code(pattern, message)
        print(f'OTP: {Colors.LPURPLE}{otp}{Colors.END}')

        token = self.__complete_signup(email, otp)
        id_token = self.__verify_token(token)
        self.__verify_email(id_token)
        result_info = self.__get_result_info(id_token)

        result = {
            'firstname': first_name,
            'lastname': last_name,
            'email': email,
            'created': result_info['created'],
            'role': result_info['role'],
            'apikey': result_info['apikey'],
            'apikey_usage': result_info['apikey_usage'],
            'plan': result_info['plan'],
        }

        print(json.dumps(result, indent=4))

        #! Optional (Uncomment if you want to use it)
        # delete_mailbox = self.get_user_input('Do you want to clear the mailbox? (y/n): ', ['y', 'n'])
        # if delete_mailbox == 'y':
        #     if self.delete_mailbox():
        #         print(f'The mailbox associated with the email address {Colors.GREEN}{email}{Colors.END} has been deleted!')
        #     else:
        #         print(f'Failed to delete the mailbox associated with the email address {Colors.RED}{email}{Colors.END}')

        # elif delete_mailbox == 'n':
        #     print(f'{Colors.RED}The deletion of the mailbox has been skipped!{Colors.END}')

        self.close_session()


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    TestRegistration().start_register()

