import json
import time
from DrissionPage import ChromiumPage,ChromiumOptions
name =input('请你登录想要登录的账号,写你的名字，或者代号：')
do1 = ChromiumOptions()
# page = ChromiumPage(do1)
page2 = ChromiumPage(do1)
page2.get('https://www.douyin.com')
# page2.set.cookies.clear()
# time.sleep(120)
ex = input('按q退出')
cookies = page2.cookies()
with open('cookies_{}.json'.format(name),'w') as f:
    f.write(json.dumps(cookies))
print(cookies)
