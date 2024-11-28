from typing import Tuple
from abc import ABC, abstractmethod
import numpy as np


class VideoSource(ABC):
    """Abstract base class for video input sources."""
    
    @abstractmethod
    def read(self) -> Tuple[bool, np.ndarray]:
        """Read a frame from the video source.
        
        Returns:
            Tuple[bool, np.ndarray]: Success flag and frame
        """
        pass
    
    @abstractmethod
    def release(self) -> None:
        """Release the video source."""
        pass