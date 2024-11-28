from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class Detector(ABC):
    """Abstract base class for different types of detectors."""
    
    @abstractmethod
    def detect(self, frame: np.ndarray) -> Any:
        """Process a frame and return detections.
        
        Args:
            frame (np.ndarray): Input frame to process
            
        Returns:
            Any: Detection results in implementation-specific format
        """
        pass