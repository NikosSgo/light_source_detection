from PIL import ImageFilter

class ImageBlur:
    def __init__(self,radius = 2):
        self.step_name = "Размытие изображения."
        self.radius = radius

    def run(self, img):
        blured_img = img.filter(ImageFilter.GaussianBlur(radius=self.radius))
        return blured_img