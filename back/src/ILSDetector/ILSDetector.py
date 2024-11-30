from PIL import Image, ImageDraw
import numpy as np
import math


class ImageResize:
    def __init__(self):
        self.step_name = "Изменение размера изображения."

    def run(self, img,size):
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        return resized_img


def sphereToEquirectangular(pos):
    x = math.atan2(pos[1], pos[0]) / (2 * math.pi) + 0.5
    y = math.asin(pos[2]) / math.pi + 0.5
    return (x, y)

def equirectangularToSphere(pos):
  angles = (1 / 0.1591, 1 / 0.3183)
  thetaPhi = (pos[0] - 0.5, pos[1] - 0.5)
  thetaPhi = (thetaPhi[0] * angles[0], thetaPhi[1] * angles[1])

  length = math.cos(thetaPhi[1])
  return (math.cos(thetaPhi[0]) * length, math.sin(thetaPhi[0]) * length, math.sin(thetaPhi[1]))

def vdcSequence(bits):
    bits = (bits << 16) | (bits >> 16)
    bits = ((bits & 0x55555555) << 1) | ((bits & 0xAAAAAAAA) >> 1)
    bits = ((bits & 0x33333333) << 2) | ((bits & 0xCCCCCCCC) >> 2)
    bits = ((bits & 0x0F0F0F0F) << 4) | ((bits & 0xF0F0F0F0) >> 4)
    bits = ((bits & 0x00FF00FF) << 8) | ((bits & 0xFF00FF00) >> 8)
    return float(bits) * 2.3283064365386963e-10  # / 0x100000000

def hammersleySequence(i, N):
    return (float(i) / float(N), vdcSequence(i))

def sphereSample(u, v):
  PI = 3.14159265358979
  phi = v * 2.0 * PI
  cosTheta = 2.0 * u - 1.0 # map to -1,1
  sinTheta = math.sqrt(1.0 - cosTheta * cosTheta);
  return (math.cos(phi) * sinTheta, math.sin(phi) * sinTheta, cosTheta)


def computeNeighbourLuminance(lum, width, height, image_pos, local_size):
    x, y = int(image_pos[0] * width), int(image_pos[1] * height)
    half_size = local_size // 2
    x_min, x_max = max(0, x - half_size), min(width, x + half_size + 1)
    y_min, y_max = max(0, y - half_size), min(height, y + half_size + 1)

    local_luminance = lum[y_min:y_max,x_min:x_max]
    return np.mean(local_luminance)

def distance2d(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def bresenhamCheck(lum,width,height, x0, y0, x1, y1):
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

class Sample:
    """Класс для представления сэмпла."""
    def __init__(self, luminance, image_pos,sphere_pos):
        self.luminance = luminance
        self.image_pos = image_pos
        self.sphere_pos = sphere_pos

class Light:
    def __init__(self):
        pass

class ILSDetector:
    def __init__(self, img):
        self.img = img

    def find(self):
        resizer = ImageResize()
        resized_img = np.array(resizer.run(self.img,1024))
        height, width, _ = resized_img.shape

        lum = resized_img[:, :, 0] * 0.2126 + resized_img[:, :, 1] * 0.7152 + resized_img[:, :, 2] * 0.0722


        local_size = int(12)

        samples_multiplyer = 0.003
        samples = int(samples_multiplyer * width * height)

        sample_list = []
        luminanceThreshold = 255*0.6

        for i in range(0,samples):
            xi = hammersleySequence(i, samples)
            xyz = sphereSample(xi[0], xi[1])
            imagePos = sphereToEquirectangular(xyz)
            luminance = lum[int(imagePos[1] * height),int(imagePos[0] * width)]
            sample = Sample(luminance, imagePos, xyz)

            nLum = computeNeighbourLuminance(lum, width, height, sample.image_pos, local_size)
            if nLum > luminanceThreshold:
                sample_list.append(sample)

        sample_list = sorted(sample_list, key=lambda obj: obj.luminance, reverse=True)
        i=0

        euclideanThresholdPixel = 0.00001

        euclideanThreshold = float(euclideanThresholdPixel) * (width / 2048.0)
        filteredCount = len(sample_list)
        localIndices = np.empty(filteredCount)
        localIndices.fill(-1)
        for i in range(0, filteredCount):
            cpos = sample_list[i].image_pos
            if localIndices[i] == -1:
                localIndices[i] = i

                for j in range(0, filteredCount):
                    if i != j and localIndices[j] == -1 and distance2d(cpos,sample_list[j].image_pos) < euclideanThreshold:
                        localIndices[j] = i

        lights = []
        finalIndices = np.empty(filteredCount)
        finalIndices.fill(-1)
        for i in localIndices:

            sample = sample_list[int(i)]
            startPos = sample.image_pos
            if finalIndices[int(i)] == -1:
                finalIndices[int(i)] = int(i)

                light = Light()
                light.originalPos = np.array(sample.image_pos)
                light.worldPos = np.array(sample.sphere_pos)
                light.pos = np.array(sample.image_pos)
                light.luminance = sample.luminance
                light.sample_indices = []

                for j in localIndices:
                    if i != j and finalIndices[int(j)] == -1:
                        endPos = sample_list[int(j)].image_pos
                        if bresenhamCheck(lum,width,height, startPos[0], startPos[1], endPos[0], endPos[1]):
                            finalIndices[int(j)] = int(i)
                            light.sample_indices.append(int(j))

                            sampleWeight = sample_list[int(j)].luminance / sample.luminance
                            light.pos = light.pos + np.array(endPos) * sampleWeight
                            light.pos = light.pos / (1.0 + sampleWeight)

                imagePos = light.pos * np.array([1.0 / width, 1.0 / height])
                light.worldPos = equirectangularToSphere(imagePos)
                lights.append(light)

        draw = ImageDraw.Draw(self.img)

        original_pos_color = "blue"
        original_pos_width = 5
        cluster_pos_color = "cyan"
        cluster_pos_width = 2
        line_color = "black"
        i = 1

        for light in lights:
            orig_x, orig_y = light.originalPos

            pos_x, pos_y = light.pos
            draw.ellipse(
                [int(pos_x*self.img.width) - 5, int(pos_y*self.img.height) - 5, int(pos_x*self.img.width) + 5, int(pos_y*self.img.height) + 5],
                fill=cluster_pos_color,
                outline=None,
            )

            for sample_idx in light.sample_indices:
                sample = sample_list[sample_idx]
                sample_x, sample_y = sample.image_pos

                draw.line(
                    [int(orig_x*self.img.width), int(orig_y*self.img.height), int(sample_x*self.img.width), int(sample_y*self.img.height)],
                    fill=line_color,
                    width=1,
                )

                top_left = (int(sample_x * self.img.width) - cluster_pos_width,
                            int(sample_y * self.img.height) - cluster_pos_width)
                bottom_right = (int(sample_x * self.img.width) + cluster_pos_width,
                                int(sample_y * self.img.height) + cluster_pos_width)

                draw.rectangle(
                    [top_left, bottom_right],
                    fill=original_pos_color,
                    outline="red",
                    width=cluster_pos_width
                )

            top_left = (int(orig_x * self.img.width) - original_pos_width,
                        int(orig_y * self.img.height) - original_pos_width)
            bottom_right = (int(orig_x * self.img.width) + original_pos_width,
                            int(orig_y * self.img.height) + original_pos_width)
            draw.rectangle(
                [top_left, bottom_right],
                fill=original_pos_color,
                width=original_pos_width
                )

            i+=1
        self.img.show()

if __name__ == "__main__":
    input_path = "../../data/raw/image1.jpg"
    pipeline = ILSDetector(Image.open(input_path))
    pipeline.find()




