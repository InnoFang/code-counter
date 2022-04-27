import requests

session = requests.Session()


def fetch(url, to_json=False):
    for retry in range(20):
        try:
            res = session.get(url=url, verify=False, timeout=10)
            if res.status_code == 200:
                if to_json:
                    return res.json()
                else:
                    return res.text
        except:
            print('Fetch "{}" error {} time(s):'.format(url, retry))
            print('\tA network problem occurs, re-request the URL automatically.')
