import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_people():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    people_count = 0

    if ret:
        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])

                if cls == 0:   # person
                    people_count += 1

    cap.release()

    return people_count