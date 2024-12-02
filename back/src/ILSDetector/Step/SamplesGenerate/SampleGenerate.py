import math

from .Sample import Sample

def vdc_sequence(bits):
    bits = (bits << 16) | (bits >> 16)
    bits = ((bits & 0x55555555) << 1) | ((bits & 0xAAAAAAAA) >> 1)
    bits = ((bits & 0x33333333) << 2) | ((bits & 0xCCCCCCCC) >> 2)
    bits = ((bits & 0x0F0F0F0F) << 4) | ((bits & 0xF0F0F0F0) >> 4)
    bits = ((bits & 0x00FF00FF) << 8) | ((bits & 0xFF00FF00) >> 8)
    return float(bits) * 2.3283064365386963e-10  # / 0x100000000

def hammersley_sequence(i, N):
    return (float(i) / float(N), vdc_sequence(i))

def sphere_sample(u, v):
  pi = 3.14159265358979
  phi = v * 2.0 * pi
  cos_theta = 2.0 * u - 1.0
  sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
  return (math.cos(phi) * sin_theta, math.sin(phi) * sin_theta, cos_theta)

def sphere_to_equirectangular(pos):
    x = math.atan2(pos[1], pos[0]) / (2 * math.pi) + 0.5
    y = math.asin(pos[2]) / math.pi + 0.5
    return (x, y)

class SampleGenerate:
    def __init__(self):
        self.step_name = "Генерация сэмплов:"
        self.steps = []

    def add_step(self,step):
        self.steps.append(step)

    def run(self,data):
        lum_img = data["img"]
        samples_multiplyer = data["samples_multiplyer"]

        height, width = lum_img.shape
        number_samples = int(samples_multiplyer * width * height)

        sample_list = []

        for i in range(0, number_samples):
            xi = hammersley_sequence(i, number_samples)
            xyz = sphere_sample(xi[0], xi[1])
            image_pos = sphere_to_equirectangular(xyz)

            luminance = lum_img[int(image_pos[1] * height), int(image_pos[0] * width)]
            sample = Sample(luminance, image_pos, xyz)

            sample_list.append(sample)
        print(f"Сэмплов сгенерировано - {len(sample_list)}.")
        data["samples"] = sample_list
        return data
