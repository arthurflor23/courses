from PIL import Image
import numpy
import math
import time
import os

def niblackThresholding(img, k=-0.2, radius=6, d=0):
	path = "Images"
	save_path = os.path.join(path, "result_thresholding", "resultadoNiblack_radius=" + str(radius) + "_k=" + str(k) + "_d=" + str(d) + img)
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	width, height = im.size
	newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
	for M in range(width):
		for N in range(height):
			windowSize = 0
			med = 0 #média
			sig = 0 # variancia
			square = 0
			for xx in range(-radius, radius+1):
				for yy in range(-radius, radius+1):
					if(M + xx >= 0 and M + xx < width and N + yy >= 0 and N + yy < height):
						rSquare = radius*radius
						xValue = (xx)**2   #This is equal to M - (M + xx)
						yValue = (yy)**2   # this is equal to N - (N + yy)
						#print("rSquare = " + str(rSquare) + " | x = " + str(xValue) + " | y = " + str(yValue))
						#Only get the circular region around the pixel, so it'll only return (a,b) if (a - x)**2 + (b - y) **2 <= r**2
						if ((xValue + yValue) <= rSquare):
							windowSize+=1
							med+= imageArray[yy + N, xx + M]
							square += (imageArray[yy + N, xx + M])**2
			med /= windowSize
			sig = (1/windowSize) * (square - ( (1/windowSize) * (med**2) ))
			sigSqrt = math.sqrt(sig)
			T = med + (k*sigSqrt) + d
			if(imageArray[N, M] >= T):
				newImageArray[N, M] = 255
			else:
				newImageArray[N, M] = 0

	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)




begin = time.time()
niblackThresholding("Image_(4).jpg")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
