import numpy as np

class ImageToArray:
    def __init__(self):
        self.step_name = "Приведение изображения к массиву."

    def run(self, img):
        array_img = np.array(img)
        return array_img