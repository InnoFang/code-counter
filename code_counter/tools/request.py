#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import requests
from requests.adapters import HTTPAdapter
from code_counter.conf.config import Config

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=3))


def is_gitee(url):
    return url.lower().startswith('https://gitee.com')


def get_access_token_for(url):
    if is_gitee(url):
        return Config().access_tokens.gitee
    return Config().access_tokens.github


def fetch(url, to_json=False):
    access_token = get_access_token_for(url)
    if is_gitee(url):
        param = {'access_token': access_token}
        if access_token:
            res = session.get(url=url, params=param, timeout=10)
        else:
            res = session.get(url=url, timeout=10)
    else:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.v3.raw',
            'Authorization': 'token ' + access_token
        }
        if access_token:
            res = session.get(url=url, headers=headers, timeout=10)
        else:
            res = session.get(url=url, timeout=10)

    if res.status_code == 200:
        if to_json:
            return res.json()
        else:
            return res.text
    elif res.status_code in [401, 403]:
        if res.status_code == 401:
            print("Access token doesn't exist. Please re-enter or empty the access token.")
        elif res.status_code == 403:
            print('"API rate limit exceeded. Please update access token.')

        if is_gitee(url):
            Config().request_gitee_access_token()
        else:
            Config().request_github_access_token()
        if access_token == get_access_token_for(url):
            print("\nAccess token has not changed")
            exit(1)
    elif res.status_code == 404:
        print("Not Found Project.")
        exit(1)
    else:
        print("fetch `{}` failed, error code {}.", url, res.status_code)
