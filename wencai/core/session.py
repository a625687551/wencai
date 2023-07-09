# -*- coding:utf-8 -*-
import requests
import random
from wencai.core.cookies import WencaiCookie


class Session(requests.Session):
    headers = {
        "Accept": "application/json,text/javascript,*/*;q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        'Connection': 'keep-alive',
        'Content-Type': "application/x-www-form-urlencoded",
        'host': "search.10jqka.com.cn",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }

    def __init__(self, proxies=None, verify=False):
        requests.Session.__init__(self)
        self.headers.update(Session.headers)
        if proxies is not None:
            if not isinstance(proxies, (list, dict)):
                raise TypeError('proxies should be list or dict')
            if isinstance(proxies, list):
                proxies = random.choice(proxies)
        self.proxies = proxies
        self.verify = verify

    def update_headers(self, source, add_headers, force_cookies=False):
        if force_cookies:
            self.headers['hexin-v'] = WencaiCookie().getHeXinVByHttp()
        else:
            self.headers['hexin-v'] = WencaiCookie().getHexinVByJson(source=source)
        if add_headers is not None:
            if not isinstance(add_headers, dict):
                raise TypeError('update_headers should be `dict` type.')
            for k, v in add_headers.items():
                self.headers[k] = v

    def get_result(self, url, source=None, force_cookies=False, add_headers=None, **kwargs):
        self.update_headers(add_headers=add_headers, source=source, force_cookies=force_cookies)
        if self.proxies is None:
            return super(Session, self).get(url=url, **kwargs)
        else:
            return super(Session, self).get(url=url, proxies=self.proxies, verify=self.verify, **kwargs)

    def post_result(self, url, source=None, data=None, json=None, add_headers=None, force_cookies=False, **kwargs):
        self.update_headers(add_headers=add_headers, source=source, force_cookies=force_cookies)
        if self.proxies is None:
            return super(Session, self).post(url=url, data=data, json=json, **kwargs)
        else:
            return super(Session, self).post(url=url, data=data, json=json, proxies=self.proxies, verify=self.verify,
                                             **kwargs)


# if __name__ == '__main__':
#     session = Session()
#     url = "http://search.10jqka.com.cn/unifiedwap/unified-wap/v2/result/get-robot-data"
#     payload = {
#         "question": '人气排名',
#         "page": 1,
#         "perpage": 50,
#         "log_info": '{"input_type": "typewrite"}',
#         "source": "Ths_iwencai_Xuangu",
#         "version": 2.0,
#         "secondary_intent": "",
#         "query_area": "",
#         "block_list": "",
#         "add_info": '{"urp": {"scene": 1, "company": 1, "business": 1}, "contentType": "json", "searchInfo": true}'
#     }
#     res = session.post_result(url=url, data=payload)
#     print(res.text)
