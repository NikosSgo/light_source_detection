import numpy as np

from .ImageResize import ImageResize
from .SamplesGenerator import SamplesGenerator
from .SamplesFilterLuminance import SamplesFilterLuminance
from .SamplesFilterEuclidean import SamplesFilterEuclidean
from .SamplesCluster import SamplesCluster
from .LightsRender import LightsRender

class ILSDetector:
    def __init__(self, img, samples_multiplier=0.006, euclidean_threshold_pixel=0.05):
        self.img = img
        self.samples_multiplier = samples_multiplier
        self.euclidean_threshold_pixel = euclidean_threshold_pixel

    def find(self):
        #Преобразование изображения (img) -> (height, width, lum)
        resizer = ImageResize()
        resized_img = np.array(resizer.run(self.img,1024))
        height, width, _ = resized_img.shape
        lum = resized_img[:, :, 0] * 0.2126 + resized_img[:, :, 1] * 0.7152 + resized_img[:, :, 2] * 0.0722
        #Генерация сэмплов  (lum,samples_multiplier) -> (sample_list)
        sample_generator = SamplesGenerator()
        sample_list = sample_generator.Generate(lum)
        #Фильтрация по яркости (sample_list, lum) -> sample_list
        sample_filter_luminance = SamplesFilterLuminance()
        sample_list = sample_filter_luminance.filter(sample_list,lum)
        #Сортировка по яркости (sample_list) -> sample_list
        sample_list = sorted(sample_list, key=lambda obj: obj.luminance, reverse=True)
        #Фильтрация по евклидову расстоянию (sample_list, euclidean_threshold_pixel) -> (sample_list)
        euclidean_threshold = float(self.euclidean_threshold_pixel) * (width / 2048.0)
        sample_list_euclidean = SamplesFilterEuclidean()
        sample_list = sample_list_euclidean.filter(sample_list,euclidean_threshold)
        #Кластеризация сэмплов (sample_list) -> (lights)
        samples_cluster = SamplesCluster()
        lights = samples_cluster.cluster(sample_list,lum)
        #Рендер сэмплов на изображение (lights, img) -> (img)
        lights_render = LightsRender()
        img = lights_render.render(lights,self.img)

        return (lights,img)