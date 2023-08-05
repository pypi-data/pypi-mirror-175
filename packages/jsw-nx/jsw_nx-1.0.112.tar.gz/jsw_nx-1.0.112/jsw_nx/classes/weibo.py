import requests
import json
import re
from .lc_option import LcOption

API_URL = 'https://picupload.weibo.com/interface/pic_upload.php'
TARGET_RE = r'"pics":(.*)\}\}'
PIC_HOST_SM = 'https://tva1.sinaimg.cn/small/'
PIC_HOST_MW690 = 'https://tva1.sinaimg.cn/mw690/'
PIC_HOST_MW1024 = 'https://tva1.sinaimg.cn/mw1024/'
PIC_HOST_MW2048 = 'https://tva1.sinaimg.cn/mw2048/'
PIC_HOST_ORIGINAL = 'https://tva1.sinaimg.cn/large/'


class Weibo:

    @property
    def headers(self):
        return {'Cookie': f'SUB={self.token}', 'Referer': 'https://weibo.com/'}

    def __init__(self):
        lc_opt = LcOption()
        res = lc_opt.get('60f768f6d9f1465d3b1d5c43')
        self.token = res['value']

    def upload(self, filepath):
        filename = open(filepath, 'rb')
        res = requests.post(API_URL, files={'pic1': filename, }, headers=self.headers)
        html = res.text
        target_str = re.findall(TARGET_RE, html)[0]
        json_data = json.loads(target_str)
        picdata = json_data['pic_1']
        is_success = picdata['width'] > 0

        if is_success:
            return {
                'success': True,
                'url': PIC_HOST_ORIGINAL + picdata['pid'] + '.jpg',
                'sm': PIC_HOST_SM + picdata['pid'] + '.jpg',
                **picdata
            }
        else:
            return {
                'success': False,
                'url': None,
                **picdata
            }
