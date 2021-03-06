from .envtype import SANDBOX
import json
import requests


class Client:
    """
    A basic driver
    """

    def __init__(self,
                 client_key,
                 server_key,
                 environment_type=SANDBOX):

        self.environment_type = environment_type
        self.client_key = client_key
        self.server_key = server_key

    def call(self, method, full_url, parameters=dict()):
        payload = json.dumps(parameters)
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        response = requests.request(
            method,
            full_url,
            auth=(self.server_key, ''),
            data=payload,
            headers=headers,
            allow_redirects=True
        ).json()

        if response.get('status_code') != None and response['status_code'] == '404':
            raise TransactionNotFound(response['status_message'])

        if response.get('status_code') != None and response['status_code'] == '406':
            raise DuplicateOrderID(response['status_message'])

        return response

    def __repr__(self):
        return ("<Midtrans.Client({0})>".format(self.environment_type.envname))


class TransactionNotFound(Exception):
    pass

class DuplicateOrderID(Exception):
    pass

