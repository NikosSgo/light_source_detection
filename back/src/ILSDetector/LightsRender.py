from PIL import ImageDraw

class LightsRender:
    def __init__(self):
        pass

    def render(self,lights,img):
        draw = ImageDraw.Draw(img)

        line_color = "black"

        sample_color = "red"
        sample_width = 5

        original_pos_color = "blue"
        original_pos_width = 10

        end_pos_color = "cyan"
        end_pos_width = 5


        for light in lights:
            orig_x, orig_y = light.image_pos

            for sample in light.rays_ends:
                sample_x, sample_y = sample.image_pos

                draw.line(
                    [int(orig_x * img.width), int(orig_y * img.height), int(sample_x * img.width),
                     int(sample_y * img.height)],
                    fill=line_color,
                    width=1,
                )

                top_left = (int(sample_x * img.width) - sample_width,
                            int(sample_y * img.height) - sample_width)
                bottom_right = (int(sample_x * img.width) + sample_width,
                                int(sample_y * img.height) + sample_width)

                draw.rectangle(
                    [top_left, bottom_right],
                    fill=original_pos_color,
                    outline=sample_color,
                    width=sample_width
                )

            top_left = (int(orig_x * img.width) - original_pos_width,
                        int(orig_y * img.height) - original_pos_width)
            bottom_right = (int(orig_x * img.width) + original_pos_width,
                            int(orig_y * img.height) + original_pos_width)
            draw.rectangle(
                [top_left, bottom_right],
                fill=original_pos_color,
                width=original_pos_width
            )
            pos_x, pos_y = light.end_pos
            draw.ellipse(
                [int(pos_x * img.width) - end_pos_width, int(pos_y * img.height) - end_pos_width, int(pos_x * img.width) + end_pos_width,
                 int(pos_y * img.height) + end_pos_width],
                fill=end_pos_color,
                outline=None,
            )

        img.show()
        return img