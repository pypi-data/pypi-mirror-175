import requests
import urllib
import hashlib
from .lc_option import LcOption

API_URL = 'https://pan.baidu.com/api'


class BaiduPan:
    @property
    def headers(self):
        return {"Cookie": self.token, }

    def __init__(self, token=None):
        self.token = token or LcOption().get_value('636484ab9c1aea6e1d70952d')

    def upload(self, **kwargs):
        source = kwargs.get('source')
        dest = kwargs.get('dest')
        res1 = self.precreate()
        uploadid = res1['uploadid']
        res2 = self.superfile2(uploadid, source)
        res3 = self.create(uploadid, source, dest)
        return res3.json()

    def precreate(self):
        url = API_URL + '/precreate'
        res = requests.post(
            url,
            headers=self.headers,
            data={'path': '/db.file', 'autoinit': 1, 'block_list': '[""]'}
        )
        return res.json()

    def superfile2(self, uploadid, filename):
        base_url = 'https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2'
        params = {
            'method': 'upload',
            'app_id': '250528',
            'path': '/',
            'uploadid': uploadid,
            'uploadsign': 0,
            'partseq': 0
        }
        url = base_url + '?' + urllib.parse.urlencode(params)
        filep = open(filename, 'rb')

        # update headers
        return requests.post(
            url,
            headers=self.headers,
            files={'file': filep, },
        )

    def create(self, uploadid, filename, remote_path):
        # get md5 from filep
        filep = open(filename, 'rb')
        md5 = hashlib.md5(filep.read()).hexdigest()
        filesize = filep.tell()
        url = API_URL + '/create'

        return requests.post(
            url,
            headers=self.headers,
            data={
                'path': remote_path,
                'size': filesize,
                'uploadid': uploadid,
                'block_list': '["' + md5 + '"]'
            }
        )
