import boto3
import math
import random
import string

from core import configuration
from core.errors import CognitoError

from marshmallow import fields

import logging
logger = logging.getLogger(__name__)

ADMIN_CREATE_USER = 'admin_create_user'
DESCRIBE_USER_POOL = 'describe_user_pool'

APP_CLIENT_NAME = 'users'


def open_cognito_connection():
    return boto3.client('cognito-idp')


def send_cognito_command(command, arguments=None):
    logger.debug("Sending Cognito command '%s'" % command,
                 extra={'arguments': arguments})

    try:
        client = open_cognito_connection()
        user_pool_id = configuration.get_setting('COGNITO_USER_POOL_USERS_ID')
        if arguments is None:
            arguments = {}

        response = getattr(client, command)(
            UserPoolId=user_pool_id,
            **arguments
        )
    except Exception as e:
        logger.error("Error sending command to Cognito: %s" % str(e))
        raise CognitoError()

    return response


def get_userpool_passwordpolicy():
    pool_details = describe_user_pool()
    return pool_details['UserPool']['Policies']['PasswordPolicy']


def describe_user_pool():
    return send_cognito_command(DESCRIBE_USER_POOL)


def generate_random_password():
    # Using the password policy rules generate a random password
    password_policy = get_userpool_passwordpolicy()

    min_length = password_policy.get('MinimumLength')
    require_uppercase = password_policy.get('RequireUppercase')
    require_lowercase = password_policy.get('RequireLowercase')
    require_numbers = password_policy.get('RequireNumbers')
    require_symbols = password_policy.get('RequireSymbols')

    chars = string.ascii_lowercase
    new_pass = ''.join(random.choice(chars) for x in range(min_length))

    if require_uppercase:
        index = int(math.ceil(min_length * .2))
        uppers = ''.join(random.choice(string.ascii_uppercase) for x in range(2))
        new_pass = new_pass[:index] + uppers + new_pass[index + 2:]

    if require_numbers:
        index = int(math.ceil(min_length * .5))
        numbers = ''.join(random.choice(string.digits) for x in range(2))
        new_pass = new_pass[:index] + numbers + new_pass[index + 2:]
    if require_numbers:
        chars += string.digits

    if require_symbols:
        index = int(math.ceil(min_length * .8))
        numbers = ''.join(random.choice(string.punctuation) for x in range(2))
        new_pass = new_pass[:index] + numbers + new_pass[index + 2:]

    if require_lowercase:
        lower_flag = any(c.islower() for c in new_pass)

        if not lower_flag:
            lower_char = ''.join(random.choice(string.ascii_lowercase) for x in range(1))
            new_pass = lower_char + new_pass[1:]

    lst_pass = list(new_pass)
    random.shuffle(lst_pass)
    new_pass = ''.join(lst_pass)
    return new_pass


def create_cognito_user(username, password, suppress=False):
    args = {
        'Username': username,
        'TemporaryPassword': password
        # 'UserAttributes': [
        #     {
        #         'Name': 'email',
        #         'Value': username
        #     },
        #     {
        #         'Name': 'email_verified',
        #         'Value': 'True'
        #     },
        # ]
    }

    if suppress:
        args['MessageAction'] = 'SUPPRESS'

    # the new user will be in the FORCE_CHANGE_PASSWORD state
    result = send_cognito_command(ADMIN_CREATE_USER, arguments=args)

    return result['User']

def manage_first_login(username, old_password, new_password):

    client = open_cognito_connection()
    response = client.list_user_pools(
        MaxResults=60
    )

    # find the user pool
    user_pool_id = configuration.get_setting('COGNITO_USER_POOL_USERS_ID')
    response = client.list_user_pool_clients(
        UserPoolId=user_pool_id,
        MaxResults=60
    )
    
    for user_pool_client in response['UserPoolClients']:
        if user_pool_client['ClientName'] == APP_CLIENT_NAME: 
            client_id = user_pool_client['ClientId']
            break

    if client_id==[]:
        return

    try: 
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': old_password 
            },
        )

        if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
            response = client.admin_respond_to_auth_challenge(
                UserPoolId=user_pool_id,
                ClientId= client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ChallengeResponses={
                    'USERNAME': username,
                    'PASSWORD': old_password,
                    'NEW_PASSWORD': new_password 
                },
                Session=response['Session'],
            )
    except Exception as e:
        logger.error("Error sending command to Cognito: %s" % str(e))
        raise CognitoError()    

    # return the authentication result if this is successful
    return response['AuthenticationResult'] 

