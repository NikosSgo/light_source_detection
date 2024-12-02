import numpy as np
class Light:
    def __init__(self,sample):
        self.image_pos = np.array(sample.image_pos)
        self.end_pos = np.array(sample.image_pos)
        self.sphere_pos = np.array(sample.image_pos)
        self.luminance = sample.luminance
        self.rays_ends = []
