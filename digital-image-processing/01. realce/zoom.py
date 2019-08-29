from PIL import Image
import numpy
import time
import os

def zoom(img, n_width, n_height):
    path = "zoom"
    save_path = os.path.join(path, "result", img)

    im = Image.open(os.path.join(path, img), "r").convert('RGB')
    arr = numpy.array(im, dtype=numpy.uint8)
    n_arr = numpy.zeros((n_height, n_width, 3), dtype=numpy.uint8)

    width, height = im.size
    p_width = int(numpy.ceil(n_width / width))
    p_height = int(numpy.ceil(n_height / height))

    for y in range(height):
        for x in range(width):
            new_x = int((n_width * x) / width)
            new_y = int((n_height * y) / height)

            for resize_y in range(p_height):
                for resize_x in range(p_width):
                    n_arr[new_y+resize_y, new_x+resize_x] = arr[y, x]

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    # Image.fromarray(n_arr).show()
    Image.fromarray(n_arr).save(save_path)

begin = time.time()
zoom("Zoom_in_(1).jpg", 360, 480)
zoom("Zoom_in_(2).jpg", 2592, 1456)
zoom("Zoom_in_(3).jpg", 720, 990)

zoom("Zoom_out_(1).jpg", 271, 120)
zoom("Zoom_out_(2).jpg", 317, 500)
zoom("Zoom_out_(3).jpg", 174, 500)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")