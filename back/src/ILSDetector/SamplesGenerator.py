import numpy as np
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
  PI = 3.14159265358979
  phi = v * 2.0 * PI
  cosTheta = 2.0 * u - 1.0 # map to -1,1
  sinTheta = math.sqrt(1.0 - cosTheta * cosTheta);
  return (math.cos(phi) * sinTheta, math.sin(phi) * sinTheta, cosTheta)

def sphere_to_equirectangular(pos):
    x = math.atan2(pos[1], pos[0]) / (2 * math.pi) + 0.5
    y = math.asin(pos[2]) / math.pi + 0.5
    return (x, y)

class SamplesGenerator:
    def __init__(self):
        pass

    def Generate(self, luminance_image, samples_multiplyer = 0.006):
        height, width = luminance_image.shape
        number_samples = int(samples_multiplyer * width * height)

        sample_list = []

        for i in range(0,number_samples):
            xi = hammersley_sequence(i, number_samples)
            xyz = sphere_sample(xi[0], xi[1])
            imagePos = sphere_to_equirectangular(xyz)

            luminance = luminance_image[int(imagePos[1] * height),int(imagePos[0] * width)]
            sample = Sample(luminance, imagePos, xyz)

            sample_list.append(sample)
        print(f"Количество сэмплов после генерации {len(sample_list)}")
        return sample_list
