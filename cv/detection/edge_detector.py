import cv2
import numpy as np
from detector import Detector

class EdgeDetector(Detector):
    """Concrete implementation of edge detection using Canny."""
    
    def __init__(self, low_threshold: int = 100, high_threshold: int = 200):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
    
    def detect(self, frame: np.ndarray) -> np.ndarray:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Detect edges
        edges = cv2.Canny(gray, self.low_threshold, self.high_threshold)
        return edges