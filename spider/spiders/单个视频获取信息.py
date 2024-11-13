import sys
import time
from datetime import datetime
from pprint import pprint
from queue import Queue
import pandas as pd
import requests
import execjs
import jieba
import urllib.parse
import os
from DrissionPage import ChromiumPage,ChromiumOptions
from fake_useragent import UserAgent
import pymysql
from urllib.parse import unquote
class Pin:
    def __init__(self):
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.douyin.com/?recommend=1',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}
    def js(self, params):
        params_str = urllib.parse.urlencode(params)
        print(params_str)
        ctx = execjs.compile(open('douyin.js').read())
        print(ctx)
        a_bogus = ctx.call('getSign', params_str)
        print(a_bogus)
        params['a_bogus'] = a_bogus

    def request_url(self, cookies):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "aweme_id": "7424736021813726503",
            "update_version_code": "170400",
            "pc_client_type": "1",
            "pc_libra_divert": "Windows",
            "version_code": "190500",
            "version_name": "19.5.0",
            "cookie_enabled": "true",
            "screen_width": "1707",
            "screen_height": "960",
            "browser_language": "zh-CN",
            "browser_platform": "Win32",
            "browser_name": "Edge",
            "browser_version": "130.0.0.0",
            "browser_online": "true",
            "engine_name": "Blink",
            "engine_version": "130.0.0.0",
            "os_name": "Windows",
            "os_version": "10",
            "cpu_core_num": "16",
            "device_memory": "8",
            "platform": "PC",
            "downlink": "3.9",
            "effective_type": "4g",
            "round_trip_time": "100",
            "webid": "7431823363549054475",
            "uifid": "dca68353d0985e2a8bd3e6652fe656c462342d173f24572ea68edd0cbeddca3883697489c890b254a5e8f15355aea8f081fefdac6f95a53cedfbb4c97ab0720f203fadf5f70cc9648e7a5613bc2dfbb606a4c10ec734d88f79349985c94c0e7843f8b35e30be24103079e1719a9c300d3be6b8af2a76cb896bbd997fb3225d1b5ecf06d4f90ef118c91a0ee7c74895f1e61dc381fb3971f1b43ba74a01bfce57c76406313e7cdd227a336ac23f77170296ff3411eb768dbb65659c35d6f976be",
            "msToken": "PFYtKVDL9RAYwMgZdP1HgveB3069ll9Id4SIEpNnYbNwO0zvSZbptk9okp4AQI_lapww9SW2ZyhtY8oJwtsywpLxNQzKqhcuX_nyJy5c1q-FlhBNrk5pN1-6wIlCTZ9n5KN1SP5InEyY49UdxNhz__C8Um31iL3ZA63D7R9tOoLG23-WR8a1Sw==",
            # "a_bogus": "Efsjk7SJOo/jKdFGmO31H12UfhDlNsuyCPiKWj2TePzMY1FP78NZocbtnxLhmZgjrYpiwC1H-VlMbdncPTUsZFrpwmhvu0vWvT/5I8so/qw1aeXkgNysCL8zuwsz0Rhil/nWil45Ws0j2E95IHIuApVGS5zL5YL2SrZIp/T9cDS83PLTnn2-CrXAjwj=",
            "verifyFp": "verify_m2vhuifg_fdcd628b_adf6_8d0e_8874_a5312fa48861",
            "fp": "verify_m2vhuifg_fdcd628b_adf6_8d0e_8874_a5312fa48861"
        }
        # print('剩余评论：',self.all_comments-params['cursor'])
        self.js(params)
        self.aweme_id = params['aweme_id']
        response = requests.get("https://www.douyin.com/aweme/v1/web/aweme/detail/", params=params,
                                headers=self.headers, cookies=cookies, timeout=5)
        result = response.json()
        # pprint(result)
        se=result['aweme_detail']['author']['sec_uid']
        url = "https://www.douyin.com/user/{}".format(se)
        params = {
            'modal_id': self.aweme_id,
            # 'vid':i
        }
        response = requests.get(url, headers=self.headers, cookies=cookies, params=params, timeout=4)
        import re
        info = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', response.text)[0]
        # print(response.text)
        json_str = unquote(info)
        import json
        json_data = json.loads(json_str)
        # pprint(json_data)
        # hrefs = json_data['app']['videoDetail']['download']['urlList']
        # print(hrefs)

        # pprint(response.json())
        self.parse(result,json_data)



    def parse(self, result,json_data):
        # global cursor, has_more
        # "total": 541, 总评论

        # print(result['aweme_detai'])
        aweme_id=result['aweme_detail']['aweme_id']
        #作者头像url：
        avatar_thumb=result["aweme_detail"]["author"]["avatar_thumb"]["url_list"][0]
        #nickname
        nickname=result["aweme_detail"]["author"]["nickname"]
        statistics=result['aweme_detail']['statistics']
        #收藏
        collect_count=statistics['collect_count']
        #评论
        comment_count=statistics['comment_count']
        #分享
        share_count=statistics['share_count']
        #点赞
        digg_count=statistics['digg_count']
        #作者sec
        se=result['aweme_detail']['author']['sec_uid']
        #标题
        desc=result['aweme_detail']['desc']
        #封面url
        cover=json_data["app"]["videoDetail"]["video"]["coverUrlList"][0]
        # 打印结果
        print(f"Aweme ID: {aweme_id}")
        print(f"收藏数: {collect_count}")
        print(f"评论数: {comment_count}")
        print(f"分享数: {share_count}")
        print(f"点赞数: {digg_count}")
        print(f"作者 SEC UID: {se}")
        print(f'作者：{nickname}')
        print(f'作者封面:{avatar_thumb}')
        print(f"标题: {desc}")
        print(f"封面 URL: {cover}")




    def save(self):
        pass
    def main(self):
        import re
        aweme_id = input(
            '请输入视频链接，比如：https://www.douyin.com/video/7424736021813726503\n,https://www.douyin.com/user/MS4wLjABAAAAaCcBHb3Rhc4zxF8YkBOfHfLh6k-IWEK2l3Ne9xOXPnQ?from_tab_name=main&modal_id=7332474824440155455&vid=7426263125093125411\n,请输入:')
        if "https://www.douyin.com/video/" in aweme_id:
            match = re.search(r'video/(\d+)', aweme_id)

            if match:
                video_id = match.group(1)  # 提取数字
                print(video_id)  # 输出: 7424736021813726503
            else:
                print("没有匹配到视频 ID")
        if "https://www.douyin.com/user/" in aweme_id:
            match = re.search(r'modal_id=(\d+)', aweme_id)
            if match:
                video_id = match.group(1)  # 提取数字
                print(video_id)  # 输出: 7424736021813726503
            else:
                print("没有匹配到视频 ID")
        self.aweme_id=video_id
        import json
        try:
            n=input('输入登录账号：')
            with open('cookies{}.json'.format(n), 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                print(cookies)
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies if
                            'name' in cookie and 'value' in cookie}
            self.request_url(cookies_dict)
        except Exception as e:
            print(e)
            print('请换账号')
        # self.request_url()
if __name__ == '__main__':
    pin = Pin()
    pin.main()

