import os
import time
import random

import pandas as pd
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Actions
from queue import Queue
import threading
import pickle
import pprint
import requests
import sys
from urllib.parse import unquote
import re
import time
import json
import requests
import pandas as pd

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    'referer': 'https://www.douyin.com',
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}
class Douyin_install:
    def __init__(self):
       # self.cookies=''
        pass
    def parse(self,page):
        id=input("请输入你要下载的视频:\n")

        match = re.search(r'user/([^?&]+)', id)
        match2 = re.search(r'modal_id=([^?&]+)', id)
        if match:
            sec_user_id= match.group(1)  # 提取数字
            print(sec_user_id)  # 输出: 7424736021813726503
        if match2:
            modal_id = match2.group(1)
            print(modal_id)
        else:
            print("没有匹配到视频")
        print(modal_id)
        params = {
            'modal_id': modal_id ,
        }
        url = "https://www.douyin.com/user/{}".format(sec_user_id)
        response = requests.get(url, headers=headers, cookies=self.cookies, params=params, timeout=4)
        print(response.text)

        info = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', response.text)[0]
        # print(response.text)
        json_str = unquote(info)
        json_data = json.loads(json_str)
        hrefs = json_data['app']['videoDetail']['download']['urlList']
        print(hrefs)
        href = ''
        for mmm in hrefs:
            if 'https://v3-web.douyinvod.com' in mmm:
                href = mmm
                break
            elif 's://www.douyin.com/aweme/v1/pla' in mmm:
                href = mmm
        print(href)
        title = json_data['app']['videoDetail']['desc']
        if len(title) <= 2:
            title = str(modal_id)
        print(title)
        new_title = re.sub(r'[\\/:*?"<>|\n\r]', '', title)
        size = 0

        print('准备下载', title)

        start = time.time()  # 开始时间
        # time.sleep(1.21)
        res = requests.get(href, headers=headers, stream=True).content
        print(res)
        print(time.time() - start)
        flie = os.path.join('.\视频',str(modal_id) + '.mp4')
        # print(res.content)
        with open(flie, 'wb') as f:
            f.write(res)

    def inits(self):
        #传入查询列表
        import json
        n = input('输入登录账号：')
        with open('cookies{}.json'.format(n), 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        # page = ChromiumPage(local_port=9122, user_data_path=r'D:\data6')
        do1 = ChromiumOptions().auto_port().set_paths(local_port=9122, user_data_path=r'D:\data6')
        # page = ChromiumPage(do1)
        page = ChromiumPage(do1)
        # 清除浏览器cookie
        page.set.cookies.clear()
        for cookie in cookies:
            # 构造cookie的格式
            cookie_dict = {
                "domain": "www.douyin.com",
                "name": cookie.get("name"),
                "value": cookie.get("value"),
            }
            # 断言一下
            if 'sameSite' in cookie_dict:
                assert cookie_dict["sameSite"] in ["Strict", "Lax", "None"]
            # 一条条添加进浏览器
            page.set.cookies(cookie_dict)
        page.get('https://www.douyin.com')
        self.cookies = page.cookies().as_dict()
        self.parse(page)


if __name__ == '__main__':
    douyin = Douyin_install()
    douyin.inits()
