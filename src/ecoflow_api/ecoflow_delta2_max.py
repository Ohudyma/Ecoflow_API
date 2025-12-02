#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ecoflow Delta 2 Max REST API Library
"""

import requests
import hashlib
import hmac
import random
import time
import os
from datetime import datetime
from flatten_dict import flatten
from urllib.parse import urlencode
from urllib.parse import unquote

class EcoflowAPI:
    base_url = None
    access_key = None
    secret_key = None
    sn = None
    params = None
    log_lvl = None

    def __init__(self, *, base_url = 'https://api.ecoflow.com', sn, access_key, secret_key, log_lvl):
        self.base_url = base_url
        self.sn = sn
        self.access_key = access_key
        self.secret_key = secret_key
        self.status_code = 200
        self.log_lvl = log_lvl
        self.log_file_dir = os.path.abspath(os.curdir) + '/'
        self.log_file = self.log_file_dir + 'log.txt'

    def logger(self, log_lvl, message):
        if log_lvl == "1":
            with open(self.log_file, 'a') as log:
                current_time = str(datetime.now().strftime("%d.%m.%y %H:%M:%S"))
                log.write(f"{current_time} - {''.join(message)}\n")
        else:
            return

    def get_nonce(self):
        try:
            nonce = str(random.randrange(100000, 999999))
            message = f"Generated nonce = {nonce}"
            self.logger(self.log_lvl, message)
            return nonce
        except Exception as e:
            message = f"ERROR - Not generated nonce {e}"
            self.logger(self.log_lvl, message)

    def get_timestamp(self):
        try:
            timestamp = str(int(time.time()) * 1000)
            message = f"Generated timestamp = {timestamp}"
            self.logger(self.log_lvl, message)
            return timestamp
        except Exception as e:
            message = f"ERROR - Not generated timestamp {e}"
            self.logger(self.log_lvl, message)

    def ecoflow_reducer(self, k1, k2):
        if k1 is None:
            return k2
        else:
            if type(k2) is int:
                return f"{k1}[{k2}]"
            else:
                return f"{k1}.{k2}"

    def flatting(self, request_data):
        try:
            params = flatten(request_data, reducer = self.ecoflow_reducer, enumerate_types=(list,))
            message = f"Request data formatted/flatted successful"
            self.logger(self.log_lvl, message)
            return params
        except Exception as e:
            message = f"ERROR - Request data NOT formatted/flatted {e}"
            self.logger(self.log_lvl, message)

    def sorting(self, flatted_data):
        try:
            sorted_params = dict(sorted(flatted_data.items()))
            message = f"Formatted/flatted data sorted successful"
            self.logger(self.log_lvl, message)
            return sorted_params
        except Exception as e:
            message = f"ERROR - Formatted/flatted data NOT sorted {e}"
            self.logger(self.log_lvl, message)

    def gen_sign(self, request_data, access_key, nonce, timestamp):
        params = self.flatting(request_data=request_data)
        sorted_params = self.sorting(flatted_data=params)
        concatenate_dict = {'accessKey': self.access_key,
                            'nonce': nonce,
                            'timestamp': timestamp}
        all_params = {**sorted_params, **concatenate_dict}
        try:
            HMAC_encoded_data = hmac.new(self.secret_key.encode(),
                                         unquote(urlencode(all_params)).encode(),
                                         hashlib.sha256).hexdigest()
            message = f"HMAC generated successful"
            self.logger(self.log_lvl, message)
            return HMAC_encoded_data
        except Exception as e:
            message = f"ERROR - Problem with encoding or HMAC generation {e}"
            self.logger(self.log_lvl, message)

    def full_url(self, path):
        try:
            return f"{self.base_url}{path}"
        except Exception as e:
            message = f"ERROR - Problem with base url or path, please check {e}"
            self.logger(self.log_lvl, message)

    def request(self, method, url, request_data=None):
        nonce = self.get_nonce()
        timestamp = self.get_timestamp()
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'accessKey': self.access_key,
            'timestamp': timestamp,
            'nonce': nonce,
            'sign': str(self.gen_sign(request_data=request_data if request_data is not None else {},
                                      access_key=self.access_key,
                                      nonce=nonce,
                                      timestamp=timestamp))
        }
        try:
            response = requests.request(method,
                                        url,
                                        headers=headers,
                                        json=request_data)
            if response.status_code == self.status_code:
                response_json = response.json()
                message = f"Request to Ecoflow successful - {response_json}"
                self.logger(self.log_lvl, message)
                return response_json
            else:
                response_json = response.json()
                message = f"ERROR - Status code of request to Ecoflow is not 200, please check the log {response_json}"
                self.logger(self.log_lvl, message)
        except Exception as e:
            message = f"ERROR - Problem with base url or path, please check {e}"
            self.logger(self.log_lvl, message)

    def set_device_quota(self, request_data):
        return self.request('put',
                            url=self.full_url('/iot-open/sign/device/quota'),
                            request_data=request_data)

    def get_all_device_quotas(self, request_data):
        return self.request(method='get',
                            url=self.full_url(f"/iot-open/sign/device/quota/all?sn={self.sn}"),
                            request_data=request_data)

    def get_device_quotas(self, request_data):
        return self.request(method='post',
                            url=self.full_url('/iot-open/sign/device/quota'),
                            request_data=request_data)
