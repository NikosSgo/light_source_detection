from PIL import Image

class ImageResize:
    def __init__(self):
        self.step_name = "Изменение размера изображения."

    def run(self, img,size):
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        return resized_img