import numpy as np

def compute_neighbour_luminance(lum, width, height, image_pos, local_size):
    x, y = int(image_pos[0] * width), int(image_pos[1] * height)
    half_size = local_size // 2
    x_min, x_max = max(0, x - half_size), min(width, x + half_size + 1)
    y_min, y_max = max(0, y - half_size), min(height, y + half_size + 1)

    local_luminance = lum[y_min:y_max,x_min:x_max]
    return np.mean(local_luminance)

class SamplesFilterLuminance:
    def __init__(self):
        self.step_name = "Фильтрация по яркости сэмпла."

    def filter(self,data):
        luminance_image = data["img"]
        samples = data["samples"]

        height, width = luminance_image.shape
        local_size = int(float(12) * (width / 1024.0)) + 1

        median_luminance = np.median(luminance_image)
        std_luminance = np.std(luminance_image)
        luminance_threshold = (median_luminance + std_luminance * 0.5)*1.15

        filtered_samples =  [sample for sample in samples
                if compute_neighbour_luminance(luminance_image, width, height, sample.image_pos, local_size) > luminance_threshold
                ]
        print(f"Количество сэмплов после фильтрации - {len(filtered_samples)}.")

        data["samples"] = filtered_samples
        return data