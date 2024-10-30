id = input("请输入你要下载的视频")
import re
match = re.search(r'user/([^?&]+)', id)
match2 = re.search(r'modal_id=([^?&]+)', id)
if match:
    sec_user_id = match.group(1)  # 提取数字
    print(sec_user_id)  # 输出: 7424736021813726503
if match2:
    modal_id = match2.group(1)
    print(modal_id)
