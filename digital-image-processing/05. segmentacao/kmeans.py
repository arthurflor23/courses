from PIL import Image
from random import randint
import numpy
import math
import time
import os

def kMeans(img, groups=3):
	path = "Images"
	save_path = os.path.join(path, "result_kmeans", "resultadoKMeans_groups=" + str(groups) + "_" + img)
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	width, height = im.size
	newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
	#newImageArray = numpy.zeros((height, width, 3), dtype=numpy.uint8)  #colors
	pointAssociation = numpy.zeros((height, width), dtype=numpy.uint8)
	randomGroups = [0, 128, 255]
	newCenterPosition = numpy.zeros((groups, 2))
	while(True):
		for y in range(height):
				for x in range(width):
					minDistance = 999999
					groupValue = -1
					for i in range(groups):
						distance = abs(imageArray[y, x] - randomGroups[i])
						if(distance < minDistance):
							minDistance = distance
							groupValue = i
					if(groupValue != -1):
						pointAssociation[y, x] = groupValue
						newCenterPosition[groupValue] += [imageArray[y, x], 1]
		everythingEqual = True
		for i in range(groups):	
			numberOfElements = newCenterPosition[i, 1]
			if(numberOfElements != 0):
				newCenter = newCenterPosition[i, 0]//numberOfElements
				if(newCenter != randomGroups[i]):
					randomGroups[i] = newCenter
					everythingEqual = False
		if(everythingEqual):
			break

	for y in range(height):
		for x in range(width):
			if(pointAssociation[y, x] == 0):
				newImageArray[y, x] = 255 #(0, 255, 0)
			elif(pointAssociation[y, x] == 1):
				newImageArray[y, x] = 0 #(0, 0, 0)
			else:
				newImageArray[y, x] = 255 #(255, 0, 0)


	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)


begin = time.time()
kMeans("Image_(5).jpg")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
