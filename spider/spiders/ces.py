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
import pprint
import requests


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
# n = input('输入登录账号：')
# with open('cookies{}.json'.format(n), 'r', encoding='utf-8') as f:
#     cookies = json.load(f)
#     print(cookies)
# cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies if
#                 'name' in cookie and 'value' in cookie}

# url = "https://www.douyin.com/video/7435959498436545802"
# response = requests.get(url, headers=headers, cookies=cookies_dict)
import requests

import requests

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ar;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'douyin.com; __ac_referer=__ac_blank; UIFID_TEMP=dca68353d0985e2a8bd3e6652fe656c462342d173f24572ea68edd0cbeddca3883697489c890b254a5e8f15355aea8f081fefdac6f95a53cedfbb4c97ab0720f22c27000ea849b10d2fe776bda540b4420b947221b11f1f34ffb46a5874dbe97e03b10351794bee18437fa4ec9066205; hevc_supported=true; xgplayer_user_id=244735587970; passport_csrf_token=70f325206ca194d0bebb219e3477bd4b; passport_csrf_token_default=70f325206ca194d0bebb219e3477bd4b; fpk1=U2FsdGVkX19ui+SGLhUjEX66ZZ4T8I3Gt3Onpvi+1rrolcBhzXKb0I92GYxgdlX8ToBuWknaram7vC9IRNsoBw==; fpk2=e2dd8fac9c214f2e57aa0dea655ff030; bd_ticket_guard_client_web_domain=2; UIFID=dca68353d0985e2a8bd3e6652fe656c462342d173f24572ea68edd0cbeddca3883697489c890b254a5e8f15355aea8f081fefdac6f95a53cedfbb4c97ab0720f203fadf5f70cc9648e7a5613bc2dfbb606a4c10ec734d88f79349985c94c0e7843f8b35e30be24103079e1719a9c300d3be6b8af2a76cb896bbd997fb3225d1b5ecf06d4f90ef118c91a0ee7c74895f1e61dc381fb3971f1b43ba74a01bfce57c76406313e7cdd227a336ac23f77170296ff3411eb768dbb65659c35d6f976be; s_v_web_id=verify_m2vhuifg_fdcd628b_adf6_8d0e_8874_a5312fa48861; d_ticket=12c131fddd8f55f72721855d131b836d00220; passport_assist_user=CkEzSF9w_G6y0Xykt9TY4H_oWMHkmk_hN8jxx_oT3_sfWEC2j8zxeNs1au7j17ewRrO3CRCRmXEMSNCHsyLJurIqbxpKCjwoxhapVd8xGEAWaKMbaiHpc5hDWAL7po6sdEknKi3AWzSv22WytObNW54QZql1DpChWVpEKaK1NJI1yIEQuo_gDRiJr9ZUIAEiAQOsu9Zq; n_mh=nKCa1lI5bc0-032-mvPVsKYaHs40beiOA8koQhyPDJ4; sso_uid_tt=91782371cde856f137d2327b6da0a120; sso_uid_tt_ss=91782371cde856f137d2327b6da0a120; toutiao_sso_user=13d7d0bb6c04733281b3bab4b26f6db1; toutiao_sso_user_ss=13d7d0bb6c04733281b3bab4b26f6db1; sid_ucp_sso_v1=1.0.0-KGJhMDEyNWIzYjIzNDQ0NTI5ODAzZTFmMGRiNWNhOThjZGQxM2FlMWYKIQjQvaCG-4yNBhDbo4e5BhjvMSAMMMib7JMGOAZA9AdIBhoCaGwiIDEzZDdkMGJiNmMwNDczMzI4MWIzYmFiNGIyNmY2ZGIx; ssid_ucp_sso_v1=1.0.0-KGJhMDEyNWIzYjIzNDQ0NTI5ODAzZTFmMGRiNWNhOThjZGQxM2FlMWYKIQjQvaCG-4yNBhDbo4e5BhjvMSAMMMib7JMGOAZA9AdIBhoCaGwiIDEzZDdkMGJiNmMwNDczMzI4MWIzYmFiNGIyNmY2ZGIx; login_time=1730269660533; passport_auth_status=531decbc571e50bfb645561ec284c33a%2C; passport_auth_status_ss=531decbc571e50bfb645561ec284c33a%2C; uid_tt=e9098189e422298d0205e47f606254de; uid_tt_ss=e9098189e422298d0205e47f606254de; sid_tt=f1822446eb8ef1fe6a29322d740ccf9c; sessionid=f1822446eb8ef1fe6a29322d740ccf9c; sessionid_ss=f1822446eb8ef1fe6a29322d740ccf9c; is_staff_user=false; store-region=cn-gs; store-region-src=uid; SelfTabRedDotControl=%5B%5D; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=ef10586f2c30ce46ad1d0b0738d0234c; __security_server_data_status=1; sid_guard=f1822446eb8ef1fe6a29322d740ccf9c%7C1730269665%7C5183997%7CSun%2C+29-Dec-2024+06%3A27%3A42+GMT; sid_ucp_v1=1.0.0-KDg4NWIxYTQ3MmRiNTlmYTNiMTExM2JmNTI0YWI2NTIzODllNTM0YWMKGwjQvaCG-4yNBhDho4e5BhjvMSAMOAZA9AdIBBoCbGYiIGYxODIyNDQ2ZWI4ZWYxZmU2YTI5MzIyZDc0MGNjZjlj; ssid_ucp_v1=1.0.0-KDg4NWIxYTQ3MmRiNTlmYTNiMTExM2JmNTI0YWI2NTIzODllNTM0YWMKGwjQvaCG-4yNBhDho4e5BhjvMSAMOAZA9AdIBBoCbGYiIGYxODIyNDQ2ZWI4ZWYxZmU2YTI5MzIyZDc0MGNjZjlj; ttwid=1%7CyC122jy8OVgbTVSe1q0dJ-ea20VqOVBqtQNIG1k613w%7C1730356237%7C02675ad91fc69495366565ddf3bc0183faf82c3276c03127eaf83c96370daf27; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; dy_swidth=1707; dy_sheight=960; csrf_session_id=a06dfe109c25c31ce4168d554a3696c3; strategyABtestKey=%221731479861.479%22; is_dash_user=1; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; biz_trace_id=63fd17c8; xg_device_score=7.6883778912304805; publish_badge_show_info=%221%2C0%2C0%2C1731479862649%22; download_guide=%223%2F20241113%2F0%22; pwa2=%220%7C0%7C3%7C0%22; __ac_signature=_02B4Z6wo00f01WS8OIwAAIDBU5j80bj6DllknDwAAD4fae; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A1%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; WallpaperGuide=%7B%22showTime%22%3A1731480288096%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A22%2C%22cursor2%22%3A6%2C%22hoverTime%22%3A1731481379152%7D; __ac_nonce=0673461e3006aa1d42e60; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAU2_4Puek5Zc64rED1iC-G2nWYHvoJZymhrIJN59gQnnIi3SGwqH-UBast5BTjuXk%2F1731513600000%2F0%2F0%2F1731486941500%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAU2_4Puek5Zc64rED1iC-G2nWYHvoJZymhrIJN59gQnnIi3SGwqH-UBast5BTjuXk%2F1731513600000%2F0%2F1731486341501%2F0%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A960%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTFMydjRQd0NtY295dkRNSit4N2gxb1c3Y1hGWitCUkhsUS9TQXhQSytNRGk0ZWFXYWV4WDdHdjFCL2xxbzBSU0RldSt0MS9IOUY1UWljZXRnTUJ0ODQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; odin_tt=eed58077256ae0a77401fe0ef26c9e89043137ffbc0712203d9bb3363a9373abbef0f1a2d7f65ab1dd598d4d0e525785a597f399c72af1afa6c032d95e4ba0cf; IsDouyinActive=false; passport_fe_beating_status=false',
    'priority': 'u=0, i',
    'referer': 'https://www.douyin.com/user/MS4wLjABAAAA9hHjOjZz3mQN2js7qq5xj0o-gJYRMd7WBYfLPI4i8EbXA14QwWscFkoaRbytjEvQ?from_tab_name=main&modal_id=7410757800978058508&relation=0&vid=7424736021813726503',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
}

params = {
    'from_tab_name': 'main',
    'modal_id': '7410757800978058508',
    'relation': '0',
    'vid': '7424736021813726503',
}

response = requests.get(
    'https://www.douyin.com/user/MS4wLjABAAAA9hHjOjZz3mQN2js7qq5xj0o-gJYRMd7WBYfLPI4i8EbXA14QwWscFkoaRbytjEvQ',
    params=params,
    headers=headers,
)

info = re.findall('<script id="RENDER_DATA" type="application/json">(.*?)</script>', response.text)[0]
# print(response.text)
# pprint(response.json())
json_str = unquote(info)
json_data = json.loads(json_str)
pprint.pprint(json_data)
hrefs = json_data['app']['videoDetail']['download']['urlList']
print(hrefs)