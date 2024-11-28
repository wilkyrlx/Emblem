from typing import Tuple
import cv2
import numpy as np
from video_source import VideoSource


class WebcamSource(VideoSource):
    """Concrete implementation of VideoSource for webcam input."""
    
    def __init__(self, camera_id: int = 0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open camera {camera_id}")
    
    def read(self) -> Tuple[bool, np.ndarray]:
        return self.cap.read()
    
    def release(self) -> None:
        self.cap.release()