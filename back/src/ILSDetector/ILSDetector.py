from .Step import *
from .LightsRender import LightsRender

class ILSDetector:
    def __init__(self, img, samples_multiplier=0.006, euclidean_threshold_pixel=0.03):
        self.img = img
        self.samples_multiplier = samples_multiplier
        self.euclidean_threshold_pixel = euclidean_threshold_pixel
        self.steps = self._initialize_steps()

    def _initialize_image_transform(self):
        image_resizer, image_blur, image_to_array, image_to_lum = ImageResize(), ImageBlur(), ImageToArray(), ImageToLum()
        image_transform = ImageTransform()
        image_transform.steps = [image_resizer, image_blur, image_to_array, image_to_lum]
        return image_transform

    def _initialize_samples_generate(self):
        samples_generate = SampleGenerate()
        return samples_generate

    def _initialize_samples_filter(self):
        samples_sort = SamplesSort()
        samples_filter_luminance, samples_filter_euclidean = SamplesFilterLuminance(), SamplesFilterEuclidean()
        samples_filter = SamplesFilter()
        samples_filter.steps = [samples_filter_luminance, samples_sort, samples_filter_euclidean]
        return samples_filter

    def _initialize_samples_cluster(self):
        samples_claster = SamplesCluster()
        return samples_claster

    def _initialize_steps(self):
        image_transform_steps = self._initialize_image_transform()
        samples_generate_steps = self._initialize_samples_generate()
        samples_filter_steps = self._initialize_samples_filter()
        samples_cluster_steps = self._initialize_samples_cluster()
        steps = [image_transform_steps, samples_generate_steps, samples_filter_steps, samples_cluster_steps]
        return steps

    def find(self):
        copied_img = self.img.copy()
        data = {
            "img": self.img,
            "samples_multiplyer": self.samples_multiplier,
            "euclidean_threshold_pixel": self.euclidean_threshold_pixel,
        }
        for step in self.steps:
            print(step.step_name)
            data = step.run(data)

        lights_render = LightsRender()
        lights_render.render(data["lights"],copied_img)

        return data