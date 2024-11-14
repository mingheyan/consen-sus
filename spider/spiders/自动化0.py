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
    def check(self,page,choose):
        #查询列表
        for m in choose:
            try:
                page.ele('x://*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/div/input').clear()
                page.ele('x://*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/div/input').input('{}\n'.format(m))
                tab = page.latest_tab
                print(tab.title)
                tab.ele('@text()=用户').click()
                time.sleep(2)
                tab = page.latest_tab
                tab.ele('x://*[@id="search-content-area"]/div/div[1]/div[2]/div[3]/ul/li[1]/div/a').click()
                tab = page.latest_tab
                print(tab.url)
                pattern = r'user/([a-zA-Z0-9_-]+)'
                # 使用re.search查找匹配项
                match = re.search(pattern, tab.url)
                # 如果找到匹配项，打印结果
                if match:
                    print("匹配到的用户ID:", match.group(1))  # 使用group(1)来获取第一个括号内匹配的内容
                else:
                    print("没有找到匹配项")
                sec_user_id = match.group(1)
                self.parse(page, sec_user_id, m)
                tab.close()
                tab = page.latest_tab
                tab.close()

            except:
                try:
                    page.refresh()
                    time.sleep(2)
                    page.ele(
                        'x://*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/div/input').clear()
                    page.ele(
                        'x://*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/div/input').input(
                        '{}\n'.format(m))
                    tab = page.latest_tab
                    print(tab.title)
                    tab.ele('@text()=用户').click()
                    tab.ele('x:(//*[@class="search-result-card"])[1]').click()
                    tab2 = page.latest_tab
                    print(tab2.url)
                    pattern = r'user/([a-zA-Z0-9_-]+)'
                    # 使用re.search查找匹配项
                    match = re.search(pattern, tab2.url)
                    # 如果找到匹配项，打印结果
                    if match:
                        print("匹配到的用户ID:", match.group(1))  # 使用group(1)来获取第一个括号内匹配的内容
                    else:
                        print("没有找到匹配项")
                    sec_user_id = match.group(1)
                    self.parse(page, sec_user_id, m)
                except Exception as e:
                    print(e)
    def parse(self,page,sec_user_id,m):
        relative_path = 'blog'
        # 获取当前工作目录
        current_dir = os.getcwd()
        # 构建完整的相对路径
        file_name = os.path.join(current_dir, relative_path)
        if not os.path.exists(file_name):
            os.makedirs(file_name)
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
            cookies = page.cookies(as_dict=True)
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
                for mmm in hrefs:
                    if 'http://v3-web.douyinvod.com' in mmm:
                        href = mmm

                if 'schema_type' in url:
                    awesome_id = reuslut['aweme_list'][i]['aweme_id']
                    # 标题
                    title = reuslut['aweme_list'][i]["desc"]
                    # 评论数
                    comment = reuslut['aweme_list'][i]['statistics']['comment_count']
                    # 分享数
                    share = reuslut['aweme_list'][i]['statistics']['share_count']
                    # 喜欢
                    digg = reuslut['aweme_list'][i]['statistics']['digg_count']
                    # 收藏
                    collect = reuslut['aweme_list'][i]['statistics']['collect_count']
                    import datetime

                    timestamp = reuslut['aweme_list'][i]['create_time']
                    dt_object = datetime.datetime.fromtimestamp(timestamp)
                    print(title, awesome_id, share, digg, collect, comment, dt_object)
                    data_dict = {
                        '博主': m,
                        'URL': url,
                        'Awesome ID': awesome_id,
                        'Title': title,
                        'Comment Count': comment,
                        'Share Count': share,
                        'Digg Count': digg,
                        'Collect Count': collect,
                        'timestamp': dt_object,
                        'href': href,
                    }
                    # 将字典转换为DataFrame
                    df = pd.DataFrame([data_dict])
                    # df.to_csv('Douyin{}.csv'.format(m), index=False)
                    # 打开文件，追加数据，并写入CSV格式
                    file = os.path.join(file_name, m + '图文.csv')
                    with open(file, 'a', encoding='utf-8') as f:
                        # 写入文件头，只在第一次写入时需要
                        if f.tell() == 0:  # 如果文件指针在文件开头，说明文件是空的
                            df.to_csv(f, index=False)  # 写入文件头
                        else:
                            df.to_csv(f, index=False, header=False)  # 追加数据，不写入文件头
                        # 打印消息，表明数据已成功存入
                        print(title, '存入成功')
                    continue
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
                    '博主':m,
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
        df = pd.DataFrame(data)
        file=os.path.join(file_name, m+'.csv')
        df.to_csv(file,index=False)
    def inits(self):
        #传入查询列表

        choose=['王东来']

        m=input("是否登录，0or1\n")
        if m=='0':
            print('请转入抖音获取cookie登陆')
            sys.exit()
        else:
            co = ChromiumOptions().headless(False).set_paths(local_port=9121, user_data_path=r'D:\data5')
            page = ChromiumPage(co)
            page.get('https://www.douyin.com/?recommend=1', retry=3, interval=2, timeout=5)
            try:
                self.check(page,choose)
            finally:
                print('已经安全退出')
                page.quit()


if __name__ == '__main__':
    douyin = Douyin()
    douyin.inits()
