import glob
import os
import sys

import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def generate_thumbnail(mp4_path):
    base_path = os.path.dirname(mp4_path)
    file_name, file_ext = os.path.splitext(os.path.basename(mp4_path))
    tmp_dir = os.path.join(base_path, 'tmp', file_name)

    if file_ext != "mp4":
        return

    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(os.path.join(base_path, 'thumbnail'), exist_ok=True)

    cap = cv2.VideoCapture(mp4_path)
    if not cap.isOpened():
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    for i in range(16):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_count / 16)
        _, img = cap.read()
        w = img.shape[1]
        h = img.shape[0]
        new_w = 512
        new_h = int(h * new_w / w)
        img = cv2.resize(img, (new_w, new_h))
        cv2.imwrite(
            os.path.join(tmp_dir, f'{i}.jpg'), img)

    plt.figure(figsize=(12, 13))
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.05,
                        top=0.95, wspace=0.0, hspace=0.0)

    for i in range(16):
        tmp_img = cv2.imread(os.path.join(tmp_dir, f"{i}.jpg"))
        tmp_img = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2RGB)
        plt.subplot(4, 4, i+1)
        plt.subplots_adjust(hspace=0.0)
        plt.rcParams["font.size"] = 12
        plt.title(f"{round(i * (frame_count / fps) / 16, 1)}s")
        plt.axis('off')
        plt.imshow(tmp_img)

    plt.suptitle(
        f"{file_name}.mp4 - {round(frame_count / fps, 1)}s ({fps}fps)")
    plt.savefig(os.path.join(base_path, "thumbnail",
                f"{file_name}_thumbnail.jpg"))
    plt.clf()
    plt.close()

    remove_tmp_dir(tmp_dir)


def remove_tmp_dir(tmp_dir):
    for f in glob.glob(f"{tmp_dir}/**/*.jpg", recursive=True):
        if os.path.isfile(f):
            os.remove(f)
    try:
        os.rmdir(tmp_dir)
    except OSError:
        pass


if __name__ == "__main__":
    file_list = glob.glob(f"{sys.argv[1]}/**/*.mp4", recursive=True)
    print(f"{len(file_list)} Files")
    for f in file_list:
        print(f"{os.path.basename(f)}")
    for f in file_list:
        try:
            generate_thumbnail(f)
        except Exception:
            pass
