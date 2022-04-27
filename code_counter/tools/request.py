import requests

session = requests.Session()


def fetch(url, to_json=False):
    for retry in range(5):
        try:
            res = session.get(url=url, timeout=10)
            if res.status_code == 200:
                if to_json:
                    return res.json()
                else:
                    return res.text
            elif res.status_code == 403:
                print('"API rate limit exceeded. update AccessToken please, and then retry.')
                exit(1)
            else:
                print("fetch `{}` failed, error code {}.", url, res.status_code)
        except:
            print('Fetch "{}" error {} time(s):'.format(url, retry))
            print('\tA network problem occurs, re-request the URL automatically.')
