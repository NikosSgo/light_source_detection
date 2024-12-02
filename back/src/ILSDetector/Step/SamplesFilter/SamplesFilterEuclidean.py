import math

def distance_2d(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


class SamplesFilterEuclidean:
    def __init__(self):
        self.step_name = "Фильтрация по евклидовой метрике."

    def filter(self, data):
        samples = data["samples"]
        euclidean_threshold_pixel = data["euclidean_threshold_pixel"]
        height, width = data["img"].shape
        euclidean_threshold = float(euclidean_threshold_pixel) * (width / 2048.0)

        filtered_samples = []

        for i, sample in enumerate(samples):
            is_too_close = any(
                distance_2d(sample.image_pos, filtered.image_pos) <= euclidean_threshold
                for filtered in filtered_samples
            )

            if not is_too_close:
                filtered_samples.append(sample)
        print(f"Количество сэмплов после фильтрации - {len(filtered_samples)}.")
        data["samples"] = filtered_samples
        return data

