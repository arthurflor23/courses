from PIL import Image
from pathlib import Path
from random import randint
import numpy
import math
import time
import os


class pointNodes:
	def __init__(self, val=None):
		self.val = val
		self.nextVal = None

def floodFill(imageArray, newImageArray, pointX, pointY, red, green, blue):
	height, width = imageArray.shape
	nodePoint = pointNodes(numpy.array([pointY, pointX]))
	numberOfPoints = 0
	while(nodePoint):
		xx = nodePoint.val[1]
		yy = nodePoint.val[0]
		if(yy < 0 or yy > height or xx < 0 or xx > width):
			nodePoint = nodePoint.nextVal
		elif imageArray[yy, xx] > 50:
			numberOfPoints +=1
			colorRed = (imageArray[yy, xx] * red)/255
			colorGreen = (imageArray[yy, xx] * green)/255
			colorBlue = (imageArray[yy, xx] * blue)/255
			imageArray[yy, xx] = 0
			newImageArray[yy, xx] = (colorRed, colorGreen, colorBlue)
			nodeWest = pointNodes(numpy.array([yy, xx-1]))
			nodeEast = pointNodes(numpy.array([yy, xx+1]))
			nodeNorth = pointNodes(numpy.array([yy-1, xx]))
			nodeSouth = pointNodes(numpy.array([yy+1, xx]))
			nodeWest.nextVal = nodeEast
			nodeEast.nextVal = nodeNorth
			nodeNorth.nextVal = nodeSouth
			nodeSouth.nextVal = nodePoint.nextVal
			nodePoint = nodeWest
		else:
			nodePoint = nodePoint.nextVal
	print(numberOfPoints)
	return newImageArray

def colorImage(img):
	path = "data"
	filesPath = Path("out/files/" + img[:-4] + "/")
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	height, width = imageArray.shape
	newImageArray = numpy.zeros((height, width, 3), dtype=numpy.uint8)  #colors
	for yy in range(height):
		for xx in range(width):
			value = imageArray[yy, xx]
			newImageArray[yy, xx] = (value, value, value)
	newImageArray = floodFill(imageArray, newImageArray, 305, 150, 255, 255, 0) # head
	newImageArray = floodFill(imageArray, newImageArray, 245, 561, 255, 255, 0) # arm1
	newImageArray = floodFill(imageArray, newImageArray, 579, 505, 255, 255, 0) # arm2
	newImageArray = floodFill(imageArray, newImageArray, 353, 772, 255, 255, 0) # leg1
	newImageArray = floodFill(imageArray, newImageArray, 585, 763, 255, 255, 0) # leg2
	newImageArray = floodFill(imageArray, newImageArray, 486, 556, 255, 128, 0) # shirt
	newImageArray = floodFill(imageArray, newImageArray, 514, 483, 255, 128, 0) # shirt2
	newImageArray = floodFill(imageArray, newImageArray, 359, 880, 0, 255, 255) # shoe1
	newImageArray = floodFill(imageArray, newImageArray, 674, 812, 0, 255, 255) # shoe2
	newImageArray = floodFill(imageArray, newImageArray, 554, 659, 0, 255, 255) # pants
	newImageArray = floodFill(imageArray, newImageArray, 108, 604, 255, 0, 0) # spray
	newImageArray = floodFill(imageArray, newImageArray, 62, 530, 255, 0, 0) # spray
	save_path = os.path.join(filesPath, "resultBartFloodFill.png")
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)




#this one doesn't work, but I didn't want to delete it, so here it is
def floodFillRecursive(imageArray, newImageArray, pointX, pointY):
	height, width = imageArray.shape
	if(pointX < 0 or pointX > width or pointY < 0 or pointY > height):
		return
	if(imageArray[pointY, pointX] < 50):
		return
	newImageArray[pointY, pointX] = (255, 255, 0)
	floodFillRecursive(imageArray, newImageArray, pointX+1, pointY)
	floodFillRecursive(imageArray, newImageArray,pointX-1, pointY)
	floodFillRecursive(imageArray, newImageArray,pointX, pointY+1)
	floodFillRecursive(imageArray, newImageArray,pointX, pointY-1)
	

def median(imageArray, r):
	height, width = imageArray.shape
	newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
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
	return newImageArray

def fatiamento(img):
	path = "data"
	filesPath = Path("out/files/" + img[:-4] + "/")
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	#imageArray = median(imageArray, 2)
	width, height = im.size
	newImageArray = numpy.zeros((height, width, 3), dtype=numpy.uint8)  #colors
	for yy in range(height):
		for xx in range(width):
			if(imageArray[yy, xx] < 64):
				newImageArray[yy, xx] = (0, 0, 0) # black
			elif(imageArray[yy, xx] >= 64 and imageArray[yy, xx] < 128):
				newImageArray[yy, xx] = (0, 255, 255) # cyan
			elif(imageArray[yy, xx] >= 128 and imageArray[yy, xx] < 192):
				newImageArray[yy, xx] = (255, 128, 0) # orange
			elif(imageArray[yy, xx] >= 192):
				newImageArray[yy, xx] = (255, 255, 0) # yellow
	save_path = os.path.join(filesPath, "resultBartFatiamento.png")
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)

def kMeans(img):
	path = "data"
	filesPath = Path("out/files/" + img[:-4] + "/")
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	width, height = im.size
	newImageArray = numpy.zeros((height, width, 3), dtype=numpy.uint8)  #colors
	pointAssociation = numpy.zeros((height, width), dtype=numpy.uint8)
	randomGroups = [0, 85, 170, 255]
	#randomGroups = [0, 25, 50, 75, 100, 125, 150, 175, 255]
	groups = len(randomGroups)
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
				newImageArray[y, x] = (0, 0, 0) # black
			elif(pointAssociation[y, x] == 1):
				newImageArray[y, x] = (0, 255, 255) # cyan
			elif(pointAssociation[y, x] == 2):
				newImageArray[y, x] = (255, 128, 0) # orange
			elif(pointAssociation[y, x] == 3):
				newImageArray[y, x] = (255, 255, 0) # yellow

	save_path = os.path.join(filesPath, "resultBartKMeans.png")
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)


begin = time.time()
#fatiamento("Image_(3a).jpg")
colorImage("Image_(3a).jpg")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
