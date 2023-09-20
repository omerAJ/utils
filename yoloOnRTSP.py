import time
import numpy as np
from collections import defaultdict
import cv2
from ultralytics import YOLO

rtsp_url = "rtsp://user:password@xx.xx.xx.xx"
path_to_model = "../yolov8m.pt"

model = YOLO(path_to_model)


cap = cv2.VideoCapture(rtsp_url)
print('cap: ', cap)
_fps= int(cap.get(cv2.CAP_PROP_FPS))
print("_fps: ", _fps)
cv2.namedWindow('track', cv2.WINDOW_NORMAL)
cv2.resizeWindow("track", (3840, 2160))

num_frames = 0
start_time=time.time()
# Store the track history
track_history = defaultdict(lambda: [])

while cap.isOpened():
    ret, frame = cap.read()

    num_frames+=1
    if num_frames%100==0:
        end_time=time.time()
        fps = num_frames / (end_time-start_time)
        print("fps: ", fps)
    results = model.track(frame, verbose=False, persist=True, conf=0.3, iou=0.8, max_det=300, half=False, imgsz=640)
    # Get the boxes and track IDs

    try:
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()
    except Exception as e:
        # print("missed result: ", e)
        continue
    ano_frame = results[0].plot()

    # Plot the tracks
    for box, track_id in zip(boxes, track_ids):
        x, y, w, h = box
        track = track_history[track_id]
        track.append((float(x), float(y)))  # x, y center point
        if len(track) > 30:  # retain 90 tracks for 90 frames
            track.pop(0)

        # Draw the tracking lines
        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(ano_frame, [points], isClosed=False, color=(0, 255,0), thickness=3)

    cv2.imshow('tracking', ano_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
