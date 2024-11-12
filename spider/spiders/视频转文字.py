from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import pandas as pd
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import tkinter as tk
from tkinter import filedialog
# 设置 FFmpeg 的路径
# os.environ["PATH"] += os.pathsep + r"D:\syh\ffmpeg-2024-10-13-git-e347b4ff31-essentials_build\bin"
from loguru import logger


def select_file():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    # file_path = filedialog.askopenfilename()  # 打开文件选择对话框
    folder_path = filedialog.askdirectory()
    return folder_path

def create_folder(folder_path):
    current_directory = os.getcwd()
    new_folder_path = os.path.join(current_directory, folder_path)
    os.makedirs(new_folder_path, exist_ok=True)
    return new_folder_path


    # 读取 mp4 文件
#folder_path'C:\\Users\\32154\\Desktop\\舆论系统\\consen-sus-master\\consen-sus-master\\spider\\spiders\\viedo\\aa'
#mp3path'C:\\Users\\32154\\Desktop\\舆论系统\\consen-sus-master\\consen-sus-master\\spider\\spiders\\mp3'
def read_mp4(folder_path,mp3path):
    repeat = pd.read_csv('去重/去重.csv')
    repeat = repeat['已转文件'].to_list()
    # 模拟数据
    result = 'ssss'
    data = os.walk(folder_path)
    # 开始遍历
    for path, folder_list, file_list in data:
        for file_name in file_list:
            # 创建文件夹
            temp = path.rsplit('\\', 2)
            root = temp[0]
            dir = temp[-1]
            path_mu = os.path.join(root, '转文字结果', dir)
            if not os.path.isdir(path_mu):
                os.mkdir(path_mu)
            file_abs_path = os.path.join(path, file_name)
            ext = file_abs_path.rsplit(".", 1)[-1]
            file_name = file_name.replace('.mp4', '')
            # 查找是否是mp4，并且去重成功
            if ext == "mp4" and file_name not in str(repeat):
                file_result = os.path.join(path_mu, file_name)
                mp4_to_mp3(file_abs_path,mp3path,file_result,file_name)
            else:
                logger.warning(file_name+'此视频已经下载')
            #file_path'C:\\Users\\32154\\Desktop\\舆论系统\\consen-sus-master\\consen-sus-master\\spider\\spiders\\viedo\\aa\\7298611125539573026.mp4'
            #mp3path'C:\\Users\\32154\\Desktop\\舆论系统\\consen-sus-master\\consen-sus-master\\spider\\spiders\\mp3'
            # 调用 mp4_to_mp3 函数将 mp4 文件转换为 mp3 文件


def mp4_to_mp3(path,mp3path,file_result,file_name):
    try:
        video = VideoFileClip(path)
        audio = video.audio
        # 设置生成的mp3文件路径
        targetPath = mp3path
        # 1. 获取文件名，不包含扩展名
        file_name = os.path.splitext(os.path.basename(path))[0]
        # 2. 创建新路径
        newPath = os.path.join(targetPath, f"{file_name}.mp3")
        #newpath'C:\\Users\\32154\\Desktop\\舆论系统\\consen-sus-master\\consen-sus-master\\spider\\spiders\\mp3\\7298611125539573026.mp3'
        audio.write_audiofile(newPath)
        results = model(newPath,file_result,file_name)
        return newPath
    except Exception as e:
        print(e)
        return None


    # 读取 mp3 文件
# def read_mp3(mp3_folderpath):
#     for filename in os.listdir(mp3_folderpath):
#         if filename.endswith('.mp3'):  # 检查文件是否为 mp3 格式
#             file_path = os.path.join(mp3_folderpath, filename)  # 构建完整的文件路径
#             results = model(file_path)
#     return results


def model(file_path,file_result,file_name):
    results = []
    # targetPath = '../result'
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",  # 指定了要创建的pipeline对象执行的任务
        model=model,  # 模型
        tokenizer=processor.tokenizer,  # 分词器
        feature_extractor=processor.feature_extractor,  # 特征提取器
        max_new_tokens=128,  # 最大标记数量
        chunk_length_s=30,  # 分块长度
        batch_size=12,  # 每个批次的样本数量
        return_timestamps=True,  # 是否返回时间戳
        torch_dtype=torch_dtype,  # 指定了模型输入数据的PyTorch张量数据类型
        device=device,  # 指定了模型运行的设备
    )

    # dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
    # result = dataset[0]["audio"]
    result = pipe(file_path, generate_kwargs={"language": "zh"})
    print(result["text"])
    with open(file_result, "w") as f:
        f.write(result)
        # 保存文件
    with open('去重/去重.csv', 'a', encoding='utf-8') as f:
        if f.tell() == 0:  # 如果文件指针在文件开头，说明文件是空的
            f.write(file_name + "\n")  # 写入文件头
        f.write(file_name + '\n')  # 追加数据
    logger.success(file_name + '存入成功')
    os.remove(file_path)
    return results

def to_csv(result):
    df = pd.DataFrame({"text": result})
    df.to_csv("result.csv", index=False)


if __name__ == '__main__':
    folder_path = r'C:\Users\32154\Desktop\舆论系统\consen-sus-master\consen-sus-master\spider\spiders\viedo'  # 替换为你的文件夹路径
    mp3_folderpath = create_folder("mp3")
    read_mp4(folder_path, mp3_folderpath)
    # results = read_mp3(mp3_folderpath)
    # to_csv(results)
