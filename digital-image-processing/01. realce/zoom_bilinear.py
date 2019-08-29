from PIL import Image
import numpy
import math
import time
import os

numpy.set_printoptions(threshold=numpy.nan)

def zoom_bi(img, newWidth, newHeight):
        path = "zoom"
        save_path = os.path.join(path, "result_bilinear", img)
        im = Image.open(os.path.join(path, img), "r")
        imageArray = numpy.array(im, dtype=numpy.uint8)
        width, height = im.size
        if(width > newWidth):
                sr = width/newWidth
        else:
                sr = (width - 1)/newWidth
        if(height > newHeight):
                sc = height/newHeight
        else:
                sc = (height-1)/newHeight
        newImageArray = numpy.zeros((newHeight, newWidth, 3), dtype=numpy.uint8)
        for y in range(newHeight):
                for x in range(newWidth):
                        rf = x * sr
                        cf = y * sc
                        r0 = math.floor(rf)
                        c0 = math.floor(cf)
                        deltaR = rf - r0
                        deltaC = cf - c0
                        if(c0 < height and r0 < width):
                        	valueA = imageArray[c0, r0] * (1 - deltaR) * (1 - deltaC)
                        else:
                        	valueA = 0
                        if(c0 < height and r0 +1 < width):
                        	valueB = imageArray[c0, r0+1] * deltaR * (1 - deltaC)
                        else:
                        	valueB = 0
                        if(c0+1 < height and r0 < width):
                        	valueC = imageArray[c0+1, r0] * (1 - deltaR) * deltaC
                        else:
                        	valueC = 0
                        if(c0+1<height and r0+1<width):                    
                        	valueD = imageArray[c0+1, r0+1] * deltaR * deltaC
                        else:
                        	valueD = 0
                        newImageArray[y, x] = valueA + valueB + valueC + valueD


        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        Image.fromarray(newImageArray).save(save_path)

begin = time.time()
zoom_bi("Zoom_in_(1).jpg", 360, 480)
zoom_bi("Zoom_in_(2).jpg", 2592, 1456)
zoom_bi("Zoom_in_(3).jpg", 720, 990)

zoom_bi("Zoom_out_(1).jpg", 271, 120)
zoom_bi("Zoom_out_(2).jpg", 317, 500)
zoom_bi("Zoom_out_(3).jpg", 174, 500)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")