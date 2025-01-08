import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np

# 62: tv, 63: laptop, 67: cell phone
TARGETED_CLASSES = [67, 62, 63]

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

# Function to extract region of interest from frame. Could be used to crop the detected object and send it to a second model for further processing
def extract_roi(frame, coords):
    """
    Extract region of interest from frame given coordinates (x1, y1, x2, y2)
    Returns the extracted image region
    """
    x1, y1, x2, y2 = map(int, coords)
    return frame[y1:y2, x1:x2].copy()


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]

        detections = sv.Detections.from_yolov8(result)
        detections = detections[np.isin(detections.class_id, TARGETED_CLASSES)]

        if len(detections) != 0:
            roi = extract_roi(frame, detections.xyxy[0])
            cv2.imshow("ROI", roi)


        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )
        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break


if __name__ == "__main__":
    main()