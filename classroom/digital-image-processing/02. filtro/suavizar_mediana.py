from PIL import Image
import numpy
import math
import time
import os

numpy.set_printoptions(threshold=numpy.nan)

def median(img, r):
        path = "suavizar"
        size = (2*r) + 1
        extension =  ( "_result_mediana_" + str(size) + "x" + str(size) + "." )
        save_path = os.path.join(path, img.replace(".", extension))

        im = Image.open(os.path.join(path, img), "r")
        imageArray = numpy.array(im, dtype=numpy.uint8)
        width, height = im.size
        newImageArray = numpy.zeros((height, width, 3), dtype=numpy.uint8)
        size = (2*r) + 1
        for y in range(height):
                for x in range(width):
                        arrayToOrder = []
                        for i in range(-r, r+1):
                                for j in range(-r, r+1):
                                        if(y + i >= 0 and y+i < height and x+ j >= 0 and x+j < width):
                                                arrayToOrder.append(imageArray[y+i,x+j])
                                        else:
                                                arrayToOrder.append(0)
                        arrayToOrder.sort()
                        elementN = 2*((r**2) + r)
                        newImageArray[y, x] = arrayToOrder[elementN]



        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        Image.fromarray(newImageArray).save(save_path)

begin = time.time()
median("Suavizar_(1).jpg", 1) # 3x3
median("Suavizar_(2).jpg", 1)
median("Suavizar_(1).jpg", 2) # 5x5
median("Suavizar_(2).jpg", 2)
median("Suavizar_(1).jpg", 3) # 7x7
median("Suavizar_(2).jpg", 3)
# median("Suavizar_(1).jpg", 5) # 11x11
# median("Suavizar_(2).jpg", 5)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
