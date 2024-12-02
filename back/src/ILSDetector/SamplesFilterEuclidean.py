import math

def distance_2d(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


class SamplesFilterEuclidean:
    def __init__(self):
        pass

    def filter(self, samples, euclidean_threshold):
        filtered_samples = []  # Отфильтрованные сэмплы

        for i, sample in enumerate(samples):
            # Проверяем, находится ли текущий сэмпл слишком близко к уже добавленным
            is_too_close = any(
                distance_2d(sample.image_pos, filtered.image_pos) <= euclidean_threshold
                for filtered in filtered_samples
            )

            # Если ни один из уже добавленных сэмплов не ближе порога, добавляем текущий
            if not is_too_close:
                filtered_samples.append(sample)
        print(f"Количество сэмплов после фильтрации по расстоянию {len(filtered_samples)}")
        return filtered_samples

