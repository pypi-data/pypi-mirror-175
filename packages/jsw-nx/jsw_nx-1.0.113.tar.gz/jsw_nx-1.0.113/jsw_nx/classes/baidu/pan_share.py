import requests
import string
import random


class BaiduPanShare:
    def __init__(self, token):
        self.headers = {"Cookie": token, }

    def share(self, **kwargs):
        password = kwargs.get('password', self.generate_password(4))
        fid = kwargs.get('fid')

        url = 'https://pan.baidu.com/share/set'
        res = requests.post(
            url,
            headers=self.headers,
            data={
                'period': 0,
                'pwd': password,
                'eflag_disable': 'true',
                'schannel': 4,
                'channel_list': '[]',
                'fid_list': '[%s]' % fid,
            }
        ).json()

        return {'url': res['link'], 'password': password, }

    def generate_password(self, size):
        res = ''.join(random.choices(string.ascii_lowercase +
                                     string.digits, k=size))
        return str(res)
