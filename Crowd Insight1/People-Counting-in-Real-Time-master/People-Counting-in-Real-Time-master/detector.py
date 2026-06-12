from ultralytics import YOLO

# Load model safely (downloads automatically if not present)
try:
    model = YOLO("yolov8n.pt")
    print("[INFO] YOLOv8 model loaded successfully")
except Exception as e:
    print("[ERROR] Failed to load YOLO model:", e)


def detect_people(frame):
    try:
        results = model(frame, verbose=False)

        count = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])

                if cls == 0:  # person class
                    count += 1

        return count, results

    except Exception as e:
        print("[ERROR] Detection failed:", e)
        return 0, []