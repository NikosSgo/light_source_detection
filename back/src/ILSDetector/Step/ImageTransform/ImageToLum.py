class ImageToLum:
    def __init__(self):
        self.step_name = "Преобразование изображения в яркость."

    def run(self, img):
        lum_img = img[:, :, 0] * 0.2126 + img[:, :, 1] * 0.7152 + img[:, :, 2] * 0.0722
        return lum_img