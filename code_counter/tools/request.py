#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import requests
import threading
from requests.adapters import HTTPAdapter
from code_counter.conf.config import Config
from code_counter.tools.progress import SearchingProgressBar

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=3))


def check_if_is_github(url):
    return url.lower().startswith('https://github.com')


def get_access_token_for(url):
    if check_if_is_github(url):
        return Config().access_tokens.github
    return Config().access_tokens.gitee


def fetch(url, to_json=False):
    is_github = check_if_is_github(url)
    content, status_code = fetch_content(url, is_github)
    if status_code != 200:
        should_retry = handle_error_status_code(status_code, is_github)
        if not should_retry:
            print("fetch `{}` failed, error code {}.".format(url, status_code))
            exit(1)
        # re-try to fetch content
        content, _ = fetch_content(url, is_github)
    if to_json:
        return content.json()
    return content.text


def fetch_content(url, is_github):
    access_token = get_access_token_for(url)
    if is_github:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.v3.raw',
            'Authorization': 'token ' + access_token
        }
        if access_token:
            res = session.get(url=url, headers=headers, timeout=10)
        else:
            res = session.get(url=url, timeout=10)
    else:
        param = {'access_token': access_token}
        if access_token:
            res = session.get(url=url, params=param, timeout=10)
        else:
            res = session.get(url=url, timeout=10)
    return res, res.status_code


lock = threading.Lock()


def handle_error_status_code(status_code, is_github):
    if status_code in [401, 403]:
        lock.acquire()
        if SearchingProgressBar().is_alive():
            SearchingProgressBar().pause()
        if status_code == 401:
            print("Access token doesn't exist. Please re-enter or empty the access token.")
        elif status_code == 403:
            print('"API rate limit exceeded. Please update access token.')

        if is_github:
            changed = Config().request_github_access_token()
        else:
            changed = Config().request_gitee_access_token()
        if not changed:
            print("\nAccess token has not changed")
            if SearchingProgressBar().is_alive() or SearchingProgressBar().is_paused():
                SearchingProgressBar().stop()
            lock.release()
            return False
        if SearchingProgressBar().is_paused():
            SearchingProgressBar().resume()
        lock.release()
        return True
    elif status_code == 404:
        print("Not Found Project.")
        return False
    return False
