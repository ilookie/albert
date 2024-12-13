import os
from typing import List

import cv2
import numpy as np
from dify_client import CompletionClient
from logzero import logger
from sklearn.cluster import KMeans

from ali_cdn import AliStorge

BASE_URL = "https://dapcdn.63cj.com"

api_key = os.environ.get(
    "DIFY_API_COMMENT_ANALYSIS_KEY", "app-NvFkWargjYE1HdAvgaTEX22Z"
)
base_url = os.environ.get(
    "DIFY_API_COMMENT_ANALYSIS_URL", "http://aiops-x.farlightgames.com/v1"
)

c = CompletionClient(
    api_key=api_key,
)


class FrameInfo:
    def __init__(self, frame, frame_index, frame_time):
        self.frame = frame
        self.frame_index = frame_index
        self.frame_time = frame_time

    def __str__(self):
        return (
            f"FrameInfo(frame_index={self.frame_index}, frame_time={self.frame_time})"
        )

    def __repr__(self):
        return (
            f"FrameInfo(frame_index={self.frame_index}, frame_time={self.frame_time})"
        )

    def save_keyframes(self, output_dir):
        """
        保存关键帧到指定目录
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        remote_name = f"keyframe_{self.frame_index:04d}.jpg"
        output_path = os.path.join(output_dir, remote_name)
        cv2.imwrite(output_path, self.frame)
        return output_path

    def upload_file(self, output_path) -> dict:
        try:
            with open(output_path, "rb") as f:
                files = {"file": (output_path, f, "image/jpeg")}
                file_info = c.file_upload(user="debug", files=files).json()
                return file_info

        except Exception as e:
            logger.warning(f"[Utils] upload_file({output_path}) => {e}")


class FrameExtractor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def get_frame_time(self, frame_index):
        """
        根据帧索引和帧率计算时间
        """
        time = frame_index / self.fps
        minutes = int(time // 60)
        seconds = int(time % 60)
        milliseconds = int((time % 1) * 1000)
        frame_time = f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
        return frame_time

    def preprocess_video(self):
        """
        预处理视频,提取所有帧
        """
        frames = []
        frame_count = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            frames.append(frame)  # 保存原始彩色帧
            frame_count += 1
        self.cap.release()
        logger.info(f"已提取 {len(frames)} 帧")

        return frames

    def detect_shot_boundaries(self, frames, threshold=30):
        """
        使用帧差法检测镜头边界
        """
        shot_boundaries = []
        for i in range(1, self.frame_count):
            prev_frame = cv2.cvtColor(frames[i - 1], cv2.COLOR_BGR2GRAY)
            curr_frame = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            diff = np.mean(np.abs(curr_frame.astype(int) - prev_frame.astype(int)))
            if diff > threshold:
                shot_boundaries.append(i)
        logger.info(f"检测到 {len(shot_boundaries)} 个镜头边界: {shot_boundaries}")
        return shot_boundaries

    def extract_keyframes(self) -> List[FrameInfo]:
        """
        从每个镜头中提取关键帧
        """
        frames = self.preprocess_video()
        shot_boundaries = self.detect_shot_boundaries(frames)

        keyframes = []
        for i in range(len(shot_boundaries)):
            start = shot_boundaries[i - 1] if i > 0 else 0
            end = shot_boundaries[i]

            shot_frames = frames[start:end]

            # 使用 K-means 聚类选择关键帧
            frame_features = np.array(
                [
                    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).flatten()
                    for frame in shot_frames
                ]
            )
            kmeans = KMeans(n_clusters=1, random_state=0).fit(frame_features)
            center_idx = np.argmin(
                np.sum((frame_features - kmeans.cluster_centers_[0]) ** 2, axis=1)
            )
            frame_time = self.get_frame_time(start + center_idx)
            frame_info = FrameInfo(
                frame=shot_frames[center_idx],
                frame_index=start + center_idx,
                frame_time=frame_time,
            )
            keyframes.append(frame_info)
        return keyframes


def save_keyframes(keyframes, output_dir):
    """
    保存关键帧到指定目录
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    oss = AliStorge()

    for i, keyframe in enumerate(keyframes):
        remote_name = f"keyframe_{i:04d}.jpg"
        output_path = os.path.join(output_dir, remote_name)
        cv2.imwrite(output_path, keyframe)
        oss.ali_up(output_path, output_dir)

    logger.info(f"已保存 {len(keyframes)} 个关键帧到 {output_dir}")


def get_frame_content(timestamp, files) -> str:
    if not files:
        return ""
    api_key = os.environ.get(
        "DIFY_API_COMMENT_ANALYSIS_KEY", "app-NvFkWargjYE1HdAvgaTEX22Z"
    )
    base_url = os.environ.get(
        "DIFY_API_COMMENT_ANALYSIS_URL", "http://aiops-x.farlightgames.com/v1"
    )
    try:
        c = CompletionClient(
            api_key=api_key,
        )
        c.base_url = base_url
        r = c.create_completion_message(
            inputs={"frame_timestamp": timestamp},
            response_mode="blocking",
            user="debug",
            files=files,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.warning(f"[Utils] get_frame_content({timestamp}, {files}) => {e}")
        return ""


def main():
    video_path = "video.mp4"
    output_dir = "keyframes_output"

    fe = FrameExtractor(video_path)
    keyframes = fe.extract_keyframes()
    print(keyframes)
    return

    oss = AliStorge()
    remote_name = f"keyframe_{1:04d}.jpg"
    output_path = os.path.join(output_dir, remote_name)
    ali_cdn_url = oss.ali_up(output_path, output_dir)
    image_url = BASE_URL + ali_cdn_url
    api_key = os.environ.get(
        "DIFY_API_COMMENT_ANALYSIS_KEY", "app-NvFkWargjYE1HdAvgaTEX22Z"
    )
    base_url = os.environ.get(
        "DIFY_API_COMMENT_ANALYSIS_URL", "http://aiops-x.farlightgames.com/v1"
    )
    file_info = None
    try:
        c = CompletionClient(
            api_key=api_key,
        )
        c.base_url = base_url
        with open(output_path, "rb") as f:
            files = {"file": (output_path, f, "image/jpeg")}
            file_info = c.file_upload(user="debug", files=files).json()

    except Exception as e:
        logger.warning(f"[Utils] upload_file({output_path}) => {e}")
    if not file_info:
        return
    files = [
        {
            "url": "",
            "transfer_method": "local_file",
            "type": "image",
            "upload_file_id": file_info["id"],
        }
    ]
    content = get_frame_content(timestamp="00:00:00", files=files)
    print(content)


import os
import subprocess


def extract_keyframes(video_path, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # FFmpeg 命令
    command = [
        "ffmpeg",
        "-i",
        video_path,  # 输入视频文件
        "-vf",
        "select=eq(pict_type\,I)",  # 选择关键帧
        "-vsync",
        "vfr",  # 变帧率
        os.path.join(output_dir, "keyframe_%04d.jpg"),  # 输出文件名
    ]

    # 调用 FFmpeg
    subprocess.run(command)


# 示例用法
video_file_path = "video.mp4"  # 替换为你的视频文件路径
output_directory = "keyframes"  # 输出关键帧的目录


def test():
    import re
    import subprocess

    print("11111")

    def extract_keyframe_timestamps(video_path, output_timestamp_file):
        # FFmpeg 命令
        command = [
            "ffmpeg",
            "-i",
            video_path,  # 输入视频文件
            "-vf",
            "select=eq(pict_type\,I),showinfo",  # 选择 I 帧并显示信息
            "-vsync",
            "vfr",  # 变帧率
            "-f",
            "null",
            "-",
        ]

        # 打开输出文件以写入时间戳
        with open(output_timestamp_file, "w") as timestamp_file:
            # 调用 FFmpeg
            process = subprocess.Popen(command, stderr=subprocess.PIPE, text=True)

            # 逐行读取标准错误输出
            for line in process.stderr:
                timestamp_file.write(line)  # 将输出写入文件

        # 等待 FFmpeg 进程结束
        process.wait()

    def parse_timestamps(timestamp_file):
        timestamps = []
        with open(timestamp_file, "r") as f:
            for line in f:
                match = re.search(r"pts_time: (\d+\.\d+)", line)
                if match:
                    timestamps.append(float(match.group(1)))
        return timestamps

    # 示例用法
    video_file_path = "video.mp4"  # 替换为你的视频文件路径
    output_timestamp_file = "timestamps.txt"

    # 提取关键帧时间戳
    extract_keyframe_timestamps(video_file_path, output_timestamp_file)

    # 解析时间戳
    timestamps = parse_timestamps(output_timestamp_file)

    # 输出时间戳
    for i, ts in enumerate(timestamps):
        print(f"Keyframe {i + 1}: {ts} seconds")


if __name__ == "__main__":
    test()
