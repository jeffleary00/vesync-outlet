import re
# import hashlib
import requests
import json


"""
Usage:
    v = Vesync(username, hashed_password)

    data, response = v.get_outlets()
    if not data:
        print response.status_code

    data, response = v.turn_on(outlet_id)
    data, response = v.turn_off(outlet_id)


Initialization args:
    base_url = URL for vesync api. To date, the following two seem to work:
        - https://server1.vesync.com:4007 *default
        - https://server2.vesync.com:4007
        - https://smartapi.vesync.com

    repeats = number of times to repeat a device turn_on() or turn_off() cmd.
              sometimes, first command does not have any effect. two or three
              ensures better success. Default is 2

Jeff Leary (sillymonkeysoftware -at- gmail dot com)
"""

class Vesync(object):

    """
    init and log into vesync with credentials
    """
    def __init__(self, username, password, **kwargs):
        self.base_url = "https://server1.vesync.com:4007"
        self.repeats = 2
        self.session = requests.Session()
        self._tk = None
        self._id = None
        self._headers = {}

        allowed = ['base_url', 'repeats']
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)

        self._login(username, password)


    """
    Login, get token, set headers
    """
    def _login(self, username, password):
        # phash = hashlib.md5(password.encode('utf-8')).hexdigest()

        data = {
            'Account': username,
            'Password': password,
        }
        headers = {
            "account": username,
            "password": password,
        }

        response = self._send_request('POST', "/login", data, headers)
        if response.status_code != 200 or 'error' in response.headers:
            raise ValueError("Login failed. Check username and password")

        results = response.json()
        self._tk = results['tk']
        self._id = results['id']
        self._headers = {
            'tk': self._tk,
            'accountID': self._id,
            'id':  self._id }


    """
    send an api request

    params:
        - Request Type (PUT, GET, DELETE, POST, etc)
        - The endpoint of the request (/login, etc)
        - The JSON body payload data (optional)
        - The JSON header data (optional)

    returns:
        requests.response object
    """
    def _send_request(self, typ, endpoint, data=None, headers=None):
        s = requests.Session()

        if not headers:
            headers = self._headers

        uri = self.base_url + endpoint
        req = requests.Request(
            typ,
            uri,
            json=data,
            headers=headers,
        )
        prepared = req.prepare()
        try:
            response = s.send(prepared)
            return response
        except Exception as err:
            raise err


    """
    switch the outlet on or off:

    params:
        1. self
        2. id of the outlet/device
        3. state (0|1 (off|on))
    """
    def _switch_outlet(self, oid, state):
        data = {
            'cid': oid,
            'uri': '/relay',
            'action': 'break',
        }
        if state == 1:
            data['action'] = 'open'

        return self._send_request('POST', '/devRequest', data)


    """
    get list of all outlets

    returns:
        a tuple [data (or, None), requests.response object]
        if data is None, check response status code and messages.
    """
    def get_outlets(self, filters=['wifi-switch']):
        outlets = None
        response = self._send_request('POST', '/loadMain')
        if response.status_code == 200 and 'error' not in response.headers:
            outlets = response.json()['devices']
        else:
            return (None, response)

        if not filters:
            return (outlets, response)
        else:
            data = []
            for o in outlets:
                if o['type'] in filters:
                    data.append(o)

            return (data, response)

        return (None, response)


    """
    turn an outlet on

    a tuple [data (or, None), requests.response object]
    if data is None, check response status code and messages.
    """
    def turn_on(self, oid, repeat=None):
        response = None

        if repeat is None:
            repeat = self.repeats

        for n in range(1, repeat + 1):
            response = self._switch_outlet(oid, 1)

        return (response.json(), response)


    """
    turn an outlet off

    a tuple [data (or, None), requests.response object]
    if data is None, check response status code and messages.
    """
    def turn_off(self, oid, repeat=None):
        response = None

        if repeat is None:
            repeat = self.repeats

        for n in range(1, repeat + 1):
            response = self._switch_outlet(oid, 1)

        return (response.json(), response)
