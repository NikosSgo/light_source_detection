import math
import numpy as np

from .Light import Light

def equirectangular_to_sphere(pos):
  angles = (1 / 0.1591, 1 / 0.3183)
  theta_phi = (pos[0] - 0.5, pos[1] - 0.5)
  theta_phi = (theta_phi[0] * angles[0], theta_phi[1] * angles[1])

  length = math.cos(theta_phi[1])
  return (math.cos(theta_phi[0]) * length, math.sin(theta_phi[0]) * length, math.sin(theta_phi[1]))

def bresenham_check(lum,width,height, x0, y0, x1, y1):
    x0 = int(x0*width)
    x1 = int(x1*width)
    y0 = int(y0*height)
    y1 = int(y1*height)

    dx = x1-x0
    step_x = int((dx>0) - (dx < 0))
    dx = abs(dx) * 2

    dy = y1 - y0
    step_y = int((dy > 0) - (dy < 0))
    dy = abs(dy) * 2

    luminance_threshold = 255*0.15
    prev_lum = lum[y0][x0]
    sum_lum = 0.0
    c = 0
    if(dx >= dy):
        delta = dy - (dx * 2)
        while (x0 != x1):
            if ((delta > 0) or (delta == 0 and (step_x > 0))):
                delta -= dx
                y0 += step_y

            delta += dy
            x0 += step_x
            sum_lum = sum_lum + min(lum[y0][x0],255*1.25)
            c = c + 1
            if (abs(sum_lum / c - prev_lum) > luminance_threshold and (sum_lum / c) < 255*1):
                return 0
    else:
        delta = dx - (dy * 2)

        while (y0 != y1):
            if ((delta > 0) or (delta == 0 and (step_y > 0))):
                delta -= dy
                x0 += step_x

            delta += dx
            y0 += step_y
            sum_lum = sum_lum + min(lum[y0][x0], 255*1.25)
            c = c + 1
            if (abs(sum_lum / c - prev_lum) > luminance_threshold and (sum_lum / c) < 255*1.0):
                return 0
    return 1

class SamplesCluster:
    def __init__(self):
        self.step_name = "Объединение сэмплов в кластеры света"

    def run(self, data):
        samples = data["samples"]
        luminance_image = data["img"]
        height, width = luminance_image.shape

        added_samples = np.empty(len(samples))
        added_samples.fill(False)

        lights = []

        for i in range(len(samples)):
            sample = samples[i]

            if added_samples[i] == False:
                light = Light(sample)
                added_samples[i] = True

                for j in range(len(samples)):
                    if i!=j and added_samples[j] == False:
                        other_sample = samples[j]
                        end_pos = other_sample.image_pos

                        if bresenham_check(luminance_image, width, height, sample.image_pos[0], sample.image_pos[1], end_pos[0],end_pos[1]):
                            light.rays_ends.append(other_sample)
                            added_samples[j] = True

                            sample_weight = other_sample.luminance / sample.luminance
                            light.end_pos = light.end_pos + np.array(end_pos) * sample_weight
                            light.end_pos = light.end_pos / (1.0 + sample_weight)

                image_pos = light.end_pos * np.array([1.0 / width, 1.0 / height])
                light.sphere_pos = equirectangular_to_sphere(image_pos)
                lights.append(light)

        print(f"Количество, полученных кластеров - {len(lights)}")
        data["lights"] = lights
        return data

