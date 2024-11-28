import cv2
import numpy as np
from emblem_encoder_decoder import EmblemEncoderDecoder

class EmblemBuilder:
    """
    Builds an emblem from a 9-digit number and generates an emblem img that 
    represents said number. Uses the EmblemEncoderDecoder to determine the code 
    to use
    """

    def __init__(self):
        self.encoder_decoder = EmblemEncoderDecoder()
        self.grid_size = 3

    def build(self, number):
        if len(str(number)) != 9:
            raise ValueError(f"Number must have 9 digits")
        
        colors = self.encoder_decoder.encode(number)
        
        grid = np.zeros((self.grid_size * 50, self.grid_size * 50, 3), dtype=np.uint8)
        index = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                grid[i * 50 : (i + 1) * 50, j * 50 : (j + 1) * 50] = colors[index]
                index += 1
        return grid

# Example Usage
if __name__ == "__main__":
    number_to_encode = 223850789  # Up to 9 digits
    encoder_decoder = EmblemBuilder()
    
    # Encode the number into an emblem
    emblem = encoder_decoder.build(number_to_encode)
    cv2.imwrite("encoded_emblem.png", emblem)
    
    # Display the emblem
    cv2.imshow("Encoded Emblem", emblem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    