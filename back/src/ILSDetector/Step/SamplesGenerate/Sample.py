class Sample:
    """Класс для представления сэмпла."""
    def __init__(self, luminance, image_pos,sphere_pos):
        self.luminance = luminance
        self.image_pos = image_pos
        self.sphere_pos = sphere_pos

    def __eq__(self, other):
        return self.image_pos[0] == other.image_pos[0] and self.image_pos[1] == other.image_pos[1]

    def __ne__(self, other):
        if not isinstance(other,Sample):
            return NotImplemented
        return self.image_pos[0] != other.image_pos[0] or self.image_pos[1] != other.image_pos[1]

    def __repr__(self):
        return (f"Sample(luminance={self.luminance}, "
                f"image_pos=({self.image_pos[0]:.2f}, {self.image_pos[1]:.2f}), "
                f"sphere_pos=({self.sphere_pos[0]:.2f}, {self.sphere_pos[1]:.2f}, {self.sphere_pos[2]:.2f}))")