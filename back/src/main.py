from ILSDetector import ILSDetector
from PIL import Image

if __name__ == "__main__":
    input_path = "../data/raw/image10.jpg"
    img = Image.open(input_path)
    pipeline = ILSDetector(img)
    pipeline.find()