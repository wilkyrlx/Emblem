
import cv2

from emblem_encoder_decoder import EmblemEncoderDecoder


class EmblemParser():
    """
    Parses an emblem from a 9-digit number. Uses the EmblemEncoderDecoder to 
    decode the colors that were parsed
    """

    def __init__(self):
        self.grid_size = 3

    # TODO: will need to parse more complex images
    def parse(self, image_path):
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (self.grid_size * 50, self.grid_size * 50))

        # Extract the digits
        colors = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Get the color of the top-left pixel in the grid cell
                color = resized_image[i * 50, j * 50]
                colors.append(color)
        
        return EmblemEncoderDecoder().decode(colors)

        
if __name__ == "__main__":
    decoded_number = EmblemParser().parse("encoded_emblem.png")
    print(f"Decoded number: {decoded_number}")