import math
import numpy as np

from .Light import Light

def equirectangular_to_sphere(pos):
  angles = (1 / 0.1591, 1 / 0.3183)
  thetaPhi = (pos[0] - 0.5, pos[1] - 0.5)
  thetaPhi = (thetaPhi[0] * angles[0], thetaPhi[1] * angles[1])

  length = math.cos(thetaPhi[1])
  return (math.cos(thetaPhi[0]) * length, math.sin(thetaPhi[0]) * length, math.sin(thetaPhi[1]))

def bresenham_check(lum,width,height, x0, y0, x1, y1):
    x0 = int(x0*width)
    x1 = int(x1*width)
    y0 = int(y0*height)
    y1 = int(y1*height)

    dX = x1-x0
    stepX = int((dX>0) - (dX < 0))
    dX = abs(dX) * 2

    dY = y1 - y0
    stepY = int((dY > 0) - (dY < 0))
    dY = abs(dY) * 2

    luminanceThreshold = 255*0.15
    prevLum = lum[y0][x0]
    sumLum = 0.0
    c = 0
    if(dX >= dY):
        delta = dY - (dX * 2)
        while (x0 != x1):
            if ((delta > 0) or (delta == 0 and (stepX > 0))):
                delta -= dX
                y0 += stepY

            delta += dY
            x0 += stepX
            sumLum = sumLum + min(lum[y0][x0],255*1.25)
            c = c + 1
            if (abs(sumLum / c - prevLum) > luminanceThreshold and (sumLum / c) < 255*1):
                return 0
    else:
        delta = dX - (dY * 2)

        while (y0 != y1):
            if ((delta > 0) or (delta == 0 and (stepY > 0))):
                delta -= dY
                x0 += stepX

            delta += dX
            y0 += stepY
            sumLum = sumLum + min(lum[y0][x0], 255*1.25)
            c = c + 1
            if (abs(sumLum / c - prevLum) > luminanceThreshold and (sumLum / c) < 255*1.0):
                return 0
    return 1

class SamplesCluster:
    def __init__(self):
        pass

    def cluster(self, samples, luminance_image):
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
                        endPos = other_sample.image_pos

                        if bresenham_check(luminance_image, width, height, sample.image_pos[0], sample.image_pos[1], endPos[0],endPos[1]):
                            light.rays_ends.append(other_sample)
                            added_samples[j] = True
                            # Рассчитываем взвешенную позицию конца света
                            sampleWeight = other_sample.luminance / sample.luminance
                            light.end_pos = light.end_pos + np.array(endPos) * sampleWeight
                            light.end_pos = light.end_pos / (1.0 + sampleWeight)

                # Конечные координаты для сферической проекции
                imagePos = light.end_pos * np.array([1.0 / width, 1.0 / height])
                light.sphere_pos = equirectangular_to_sphere(imagePos)
                lights.append(light)

        return lights

