import sys
import time
from DrissionPage import ChromiumPage,ChromiumOptions
import pandas as pd
from queue import Queue
import re
from queue import Queue
import os


class Douyin:
    def __init__(self):
        pass
    def parse(self,page):
        id=input("请输入你要查询的账号")
        match = re.search(r'user/([^?&]+)', id)
        if match:
            sec_user_id= match.group(1)  # 提取数字
            print(sec_user_id)  # 输出: 7424736021813726503
        else:
            print("没有匹配到视频 ID")
        reuslut={}
        data = []
        reuslut['has_more'] =1
        reuslut['max_cursor']=0
        while reuslut['has_more'] ==1:
            max_cursor = reuslut['max_cursor']
            import requests
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
            }
            cookies = page.cookies().as_dict()
            url = "https://www.douyin.com/aweme/v1/web/aweme/post/"
            params = {
                "max_cursor": max_cursor,
                "aid": "6383",
                "sec_user_id": sec_user_id,
                "count":10000,
                "publish_video_strategy_type": "2",
            }
            try:
                response = requests.get(url, headers=headers, cookies=cookies, params=params,timeout=5)
            except Exception as e:
                print(e)
                response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=5)
            # print(response.text)
            # print(response)
            reuslut = response.json()
            #视频链接
            length = len(reuslut['aweme_list'])
            for i in range(length):
                href=''
                #分享链接完整url
                url = reuslut['aweme_list'][i]['share_url']
                #视频链接
                hrefs= reuslut['aweme_list'][i]['video']['play_addr']['url_list']
                awesome_id =reuslut['aweme_list'][i]['aweme_id']
                #标题
                title = reuslut['aweme_list'][i]["desc"]
                # 评论数
                comment = reuslut['aweme_list'][i]['statistics']['comment_count']
                #分享数
                share = reuslut['aweme_list'][i]['statistics']['share_count']
                #喜欢
                digg = reuslut['aweme_list'][i]['statistics']['digg_count']
                #收藏
                collect = reuslut['aweme_list'][i]['statistics']['collect_count']
                import datetime
                timestamp = reuslut['aweme_list'][i]['create_time']
                dt_object = datetime.datetime.fromtimestamp(timestamp)
                print(title,awesome_id, share, digg, collect,comment,dt_object)
                # 将每条记录作为一个字典添加到列表中
                data.append({
                    'URL': url,
                    'Awesome ID': awesome_id,
                    'sec_user_id':sec_user_id,
                    'Title': title,
                    'Comment Count': comment,
                    'Share Count': share,
                    'Digg Count': digg,
                    'Collect Count': collect,
                    'timestamp': dt_object,
                    'href': href,
                })

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
        self.parse(page)
        # self.cookies = page.cookies().as_dict()

if __name__ == '__main__':
    douyin = Douyin()
    douyin.inits()
