
class SamplesSort:
    def __init__(self):
        self.step_name = "Сортировка сэмплов по яркости."

    def filter(self,data):
        samples = data["samples"]
        samples = sorted(samples, key=lambda obj: obj.luminance, reverse=True)
        data["samples"] = samples
        return data