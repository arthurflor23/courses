from PIL import Image
import numpy
import math
import time
import os

#magic happens here
def calcCubic(x, a):
        if(abs(x) >= 0 and abs(x) < 1):
                value = (-a + 2) * (abs(x))**3 + (a-3) * (abs(x))**2 +1
        elif(abs(x) >=1 and abs(x) < 2):
                value = (-a * (abs(x)**3) + ((5*a)*(abs(x)**2)) - 8*a*abs(x) + (4*a) )
        else:
                value = 0
        return value

def zoom_bicubic(img, newWidth, newHeight):
        path = "zoom"
        save_path = os.path.join(path, "result_bicubico", img)
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
        a = 0.5 #control parameter, set this from 0 to 1
        for y in range(newHeight):
                for x in range(newWidth):
                        rf = x * sr #this is the x coordinate to calculate the "distance" between the points
                        cf = y * sc #same as above, but this one is the y
                        r0 = math.floor(rf)
                        c0 = math.floor(cf)
                        q = 0 # the new pixel value
                        #loops through the 16 neighbours of the new pixel
                        for m in range(0, 4):
                                v = c0 - 1 + m
                                p = 0
                                for n in range(0, 4):
                                        u = r0 - 1 + n
                                        if(v < height and u < width):
                                                p = p + imageArray[v, u] * calcCubic(rf-u, a)
                                q = q + p * calcCubic(cf - v, a)
                        newImageArray[y, x] = q



        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        Image.fromarray(newImageArray).save(save_path)

begin = time.time()
zoom_bicubic("Zoom_in_(1).jpg", 360, 480)
zoom_bicubic("Zoom_in_(2).jpg", 2592, 1456)
zoom_bicubic("Zoom_in_(3).jpg", 720, 990)

zoom_bicubic("Zoom_out_(1).jpg", 271, 120)
zoom_bicubic("Zoom_out_(2).jpg", 317, 500)
zoom_bicubic("Zoom_out_(3).jpg", 174, 500)
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
