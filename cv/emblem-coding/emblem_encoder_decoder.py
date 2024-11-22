from typing import List
import numpy as np
import cv2

class EmblemEncoderDecoder:
    """
    Basic EncoderDecoder for an Emblem. Emblem can be any 9-digit number. 
    """

    def __init__(self):
        self.colors = [
            (255, 0, 0),    # Red for digit 0
            (0, 255, 0),    # Green for digit 1
            (0, 0, 255),    # Blue for digit 2
            (255, 255, 0),  # Yellow for digit 3
            (255, 0, 255),  # Magenta for digit 4
            (0, 255, 255),  # Cyan for digit 5
            (128, 128, 128),# Gray for digit 6
            (255, 128, 0),  # Orange for digit 7
            (128, 0, 255),  # Purple for digit 8
            (0, 128, 255)   # Sky blue for digit 9
        ]

    def encode(self, number:int) -> List[int]:
        """
        Encode a number into a grid of colors.
        """
        number_str = str(number)
        colors = [self.colors[int(char)] for char in number_str]
        return colors

    def decode(self, colors: List[int]) -> int:
        """
        Decode a list of 9 colors back into the original number.
        """

        # Combine digits into the original number
        digits = map(self._color_to_digit, colors)
        return int("".join(map(str, digits)))

    def _color_to_digit(self, color):
        """
        Convert an RGB color back to its corresponding digit.
        """
        for digit, predefined_color in enumerate(self.colors):
            if np.allclose(color, predefined_color):
                return digit
        raise ValueError(f"Unrecognized color: {color}")