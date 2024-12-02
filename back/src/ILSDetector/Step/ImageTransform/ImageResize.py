from PIL import Image

class ImageResize:
    def __init__(self,size = 1024):
        self.step_name = "Изменение размера изображения."
        self.size = size

    def run(self, img):
        resized_img = img.resize((self.size, self.size), Image.Resampling.LANCZOS)
        return resized_img