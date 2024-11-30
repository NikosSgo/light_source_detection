# tests/test_steps.py
from PIL import Image
from back.src.ILSDetector.steps.ConvertToLuminance import convert_to_luminance

def test_convert_to_luminance():
    # Создаем тестовое изображение
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))  # Красное изображение

    # Преобразуем в яркость
    luminance_img = convert_to_luminance(img, apply_blur=False)

    # Проверяем, что результат имеет правильный режим и размеры
    assert luminance_img.mode == "L", "Режим изображения должен быть 'L' (оттенки серого)"
    assert luminance_img.size == img.size, "Размеры изображения должны совпадать"

    print("test_convert_to_luminance passed!")

test_convert_to_luminance()