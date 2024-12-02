class SamplesFilter:
    def __init__(self):
        self.step_name = "Фильтрация сэмплов:"
        self.steps = []

    def run(self,data):
        for filter in self.steps:
            if filter is None:
                continue
            print(filter.step_name)
            data = filter.filter(data)
        return data

