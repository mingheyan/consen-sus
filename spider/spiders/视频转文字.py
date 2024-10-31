from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import pandas as pd
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import tkinter as tk
from tkinter import filedialog
# 设置 FFmpeg 的路径
os.environ["PATH"] += os.pathsep + r"D:\syh\ffmpeg-2024-10-13-git-e347b4ff31-essentials_build\bin"




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
def read_mp4(folder_path,mp3path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp4'):  # 检查文件是否为 mp4 格式
            file_path = os.path.join(folder_path, filename)  # 构建完整的文件路径
            mp4_to_mp3(file_path,mp3path)
            # 调用 mp4_to_mp3 函数将 mp4 文件转换为 mp3 文件


def mp4_to_mp3(path,mp3path):
    try:
        video = VideoFileClip(path)
        audio = video.audio
        # 设置生成的mp3文件路径
        targetPath = mp3path
        # 1. 获取文件名，不包含扩展名
        file_name = os.path.splitext(os.path.basename(path))[0]
        # 2. 创建新路径
        newPath = os.path.join(targetPath, f"{file_name}.mp3")
        audio.write_audiofile(newPath)
        results = model(newPath)
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


def model(file_path):
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
    text_result = result["text"]
    os.remove(file_path)
    # with open()
    # results.append(text_result)
    return results
    # df = pd.DataFrame({"text": [text_result]})
    # # 1. 获取文件名，不包含扩展名
    # file_name = os.path.splitext(os.path.basename(file_path))[0]
    # # 2. 创建新路径
    # newPath = os.path.join(targetPath, f"{file_name}")
    # csv_file_path = newPath  # 指定你想要保存的路径和文件名
    # df.to_csv(csv_file_path, index=False, encoding='utf-8')  # index=False 不保存行索引


def to_csv(result):
    df = pd.DataFrame({"text": result})
    df.to_csv("result.csv", index=False)


if __name__ == '__main__':
    folder_path = select_file()  # 替换为你的文件夹路径
    mp3_folderpath = create_folder("mp3")  # 替换为你的文件路径
    read_mp4(folder_path, mp3_folderpath)
    # results = read_mp3(mp3_folderpath)
    # to_csv(results)
