from typing import Any, List

import cv2
import numpy as np
from video_source import VideoSource
from webcam_source import WebcamSource
from detector import Detector
from edge_detector import EdgeDetector

class Pipeline:
    """Main pipeline class that orchestrates the video processing."""
    
    def __init__(self, video_source: VideoSource):
        self.video_source = video_source
        self.detectors: List[Detector] = []
        
    def add_detector(self, detector: Detector) -> None:
        """Add a detector to the pipeline."""
        self.detectors.append(detector)
    
    def remove_detector(self, detector_idx: int) -> None:
        """Remove a detector from the pipeline."""
        if 0 <= detector_idx < len(self.detectors):
            self.detectors.pop(detector_idx)
    
    def process_frame(self, frame: np.ndarray) -> List[Any]:
        """Process a single frame through all detectors.
        
        Args:
            frame (np.ndarray): Input frame
            
        Returns:
            List[Any]: List of detection results from each detector
        """
        results = [frame]
        for detector in self.detectors:
            result = detector.detect(frame)
            results.append(result)
        return results
    
    def run(self, display: bool = True) -> None:
        """Run the pipeline on the video source.
        
        Args:
            display (bool): Whether to display the processed frames
        """
        try:
            while True:
                ret, frame = self.video_source.read()
                if not ret:
                    break
                
                results = self.process_frame(frame)
                
                if display:
                    # Display results - customize based on detector outputs
                    for result in results:
                        if isinstance(result, np.ndarray):  # For edge detection
                            cv2.imshow('Edges', result)
                        # Add more visualization logic for other detector types
                    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                        
        finally:
            self.video_source.release()
            cv2.destroyAllWindows()

def main():
    # Initialize video source
    video_source = WebcamSource(0)
    
    # Create pipeline
    pipeline = Pipeline(video_source)
    
    # Add edge detector
    edge_detector = EdgeDetector(low_threshold=100, high_threshold=200)
    pipeline.add_detector(edge_detector)
    
    # Add YOLO detector (commented out for now)
    # yolo_detector = YOLODetector("path/to/model")
    # pipeline.add_detector(yolo_detector)
    
    # Run pipeline
    pipeline.run()

if __name__ == "__main__":
    main()