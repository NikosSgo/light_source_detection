class ImageTransform:
    def __init__(self):
        self.step_name = "Преобразование изображения:"
        self.steps = []

    def add_step(self,step):
        self.steps.append(step)

    def run(self,data):
        img = data["img"]
        for step in self.steps:
            if step is None:
                continue
            print(step.step_name)
            img = step.run(img)
        data["img"] = img
        return data