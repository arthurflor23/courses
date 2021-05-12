from PIL import Image
import numpy
import time
import os

def isIndexValid(arr, y, x):
    if ((y >= 0 and y < len(arr)) and (x >= 0 and x < len(arr[0]))):
        return True
    else:
        return False

def getPixelRange(pixel):
    return numpy.minimum(255, numpy.maximum(0, pixel))

def sharpering(mask, arr, y, x):
    total = 0
    count = 0
    begin = -int(len(mask)/2)
    end = int(len(mask[0])/2)

    for y2 in range(begin, end+1):
        for x2 in range(begin, end+1):
            temp_y = y + y2
            temp_x = x + x2

            if (isIndexValid(arr, temp_y, temp_x)):
                mask_x = y2 - begin
                mask_y = x2 - begin
                total += (mask[mask_y, mask_x] * arr[temp_y, temp_x])
                count += 1

    return (total/count)

def suavizar(img):
    # mask = numpy.array([
        # [1, 1, 1], 
        # [1, 1, 1], 
        # [1, 1, 1], 
    # ])

    mask = numpy.array([
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1],
    ])

    path = "suavizar"
    extension = ( "_result_" + str(len(mask)) + "x" + str(len(mask[0])) + "." )
    save_path = os.path.join(path, img.replace(".", extension))

    im = Image.open(os.path.join(path, img), "r")
    arr = numpy.array(im, dtype=numpy.uint8)

    width, height = [len(arr[0]), len(arr)]
    n_arr = numpy.zeros((height, width), dtype=numpy.uint8)

    for y in range(height):
        for x in range(width):
            n_arr[y, x] = getPixelRange(sharpering(mask, arr, y, x))
            
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    # Image.fromarray(n_arr).show()
    Image.fromarray(n_arr).save(save_path)
    print("Original:\n" + str(arr) + "\n\nResultado:\n" + str(n_arr))

begin = time.time()
suavizar("Suavizar_(1).jpg")
suavizar("Suavizar_(2).jpg")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")