import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import threading
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from detector import detect_people
from alert import send_alert
from graph import prepare_graph
from config import *

video_list = [
    "videos/nirvana2.mp4",
    "videos/nirvana.mp4"
]

ALERT_INTERVAL = 10

all_data = []
frames_dict = {}
lock = threading.Lock()   # ✅ thread-safe
stop_flag = False


def process_video(video_path, cam_id):
    global stop_flag

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open {video_path}")
        return

    frame_counts = []
    last_alert_time = 0

    print(f"[INFO] Camera {cam_id} started")

    while not stop_flag:
        ret, frame = cap.read()
        if not ret:
            break

        count, results = detect_people(frame)
        frame_counts.append(count)

        for r in results:
            frame = r.plot()

        color = (0, 255, 0) if count < THRESHOLD else (0, 0, 255)

        cv2.putText(frame,
                    f"Camera {cam_id} Count: {count}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2)

        if count >= THRESHOLD:
            current_time = time.time()
            if current_time - last_alert_time > ALERT_INTERVAL:
                send_alert(cam_id, count)
                last_alert_time = current_time

        # ✅ THREAD-SAFE UPDATE
        with lock:
            frames_dict[cam_id] = frame.copy()

    cap.release()
    print(f"[INFO] Camera {cam_id} finished")

    all_data.append((cam_id, frame_counts))


def main():
    global stop_flag

    threads = []

    print("[INFO] Starting Multi-Video Processing...")

    for i, video in enumerate(video_list):
        t = threading.Thread(target=process_video, args=(video, i))
        t.start()
        threads.append(t)

    # ✅ DISPLAY LOOP
    while True:
        with lock:
            for cam_id in list(frames_dict.keys()):
                frame = frames_dict.get(cam_id, None)
                if frame is not None:
                    cv2.imshow(f"Camera {cam_id}", frame)

        key = cv2.waitKey(1)

        if key == 27:
            print("[INFO] ESC pressed → stopping cameras")
            stop_flag = True
            break

    for t in threads:
        t.join()

    cv2.destroyAllWindows()

    print("[INFO] Showing graphs...")

    if len(all_data) > 0:
        for cam_id, data in all_data:
            prepare_graph(data, cam_id)

        plt.show(block=True)
    else:
        print("[WARNING] No data to plot")


if __name__ == "__main__":
    main()