import requests


class BaiduPanShare:
    def __init__(self, token):
        self.headers = {"Cookie": token, }

    def share(self, **kwargs):
        password = kwargs.get('password', 'abcd')
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
