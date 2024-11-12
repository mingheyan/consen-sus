import os
import pandas as pd
from loguru import logger
#去重
repeat=pd.read_csv('去重/去重.csv')
repeat=repeat['已转文件'].to_list()
#模拟数据
result='ssss'
data = os.walk(r"C:\Users\32154\Desktop\舆论系统\consen-sus-master\consen-sus-master\spider\spiders\viedo")
# pa=r'C:\Users\32154\Desktop\舆论系统\consen-sus-master\consen-sus-master\spider\spiders\mp3'
#开始遍历
for path, folder_list, file_list in data:
    for file_name in file_list:
        #创建文件夹
        temp=path.rsplit('\\',2)
        root=temp[0]
        dir=temp[-1]
        path_mu=os.path.join(root,'转文字结果',dir)
        if not os.path.isdir(path_mu):
            os.mkdir(path_mu)
        file_abs_path = os.path.join(path, file_name)
        ext = file_abs_path.rsplit(".",1)[-1]
        file_name = file_name.replace('.mp4', '')
        #查找是否是mp4，并且去重成功
        if ext == "mp4" and file_name not in str(repeat):
            file_result=os.path.join(path_mu,file_name)
            #保存结果
            with open(file_result, "w") as f:
                f.write(result)
            #保存文件
            with open('去重/去重.csv', 'a', encoding='utf-8') as f:
                    if f.tell() == 0:  # 如果文件指针在文件开头，说明文件是空的
                        f.write(file_name+"\n")  # 写入文件头
                    f.write(file_name + '\n')  # 追加数据
            logger.success(file_name+'存入成功')
        else:
            logger.warning(file_name+'此视频已经转成功')



