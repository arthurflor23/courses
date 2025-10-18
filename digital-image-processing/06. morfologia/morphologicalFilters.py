from PIL import Image
import numpy
import math
import time
import os


def dilation(imageArray, dil=[[1, 1, 1], [1, 1, 1], [1, 1, 1]], center=[0,0]):
	#path = "Images"
	#im = Image.open(os.path.join(path, img), "r")
	#imageArray = numpy.array(im, dtype=numpy.uint8)
	imageShape = imageArray.shape
	width = imageShape[1]
	height = imageShape[0]
	dil = numpy.array(dil, dtype=numpy.uint8)
	#dil = numpy.ones((5,3), dtype=numpy.uint8)
	#print(str(dil))
	widthDIL, heightDIL = dil.shape
	newImageArray = numpy.full((height, width), 255, dtype=numpy.uint8)
	#save_path = os.path.join(path, "result_morph", "resultadoDilatacao_dil=" + str(dil).replace('\n','') + "_" + img)
	for x in range(width):
		for y in range(height):
			if(imageArray[y, x] < 128):
				for xx in range(widthDIL):
					for yy in range(heightDIL):
						if( (dil[xx, yy] > 0) and (yy + y - center[1]< height) and (xx + x - center[0] < width)):
							newImageArray[yy+y-center[1], xx+x-center[0]] = 0
	#os.makedirs(os.path.dirname(save_path), exist_ok=True)
	#Image.fromarray(newImageArray).save(save_path)
	return newImageArray

def erosion(imageArray, ero=[[1, 1, 1], [1, 1, 1], [1, 1, 1]], center=[0,0]):
	#path = "Images"
	#im = Image.open(os.path.join(path, img), "r")
	#imageArray = numpy.array(im, dtype=numpy.uint8)
	imageShape = imageArray.shape
	width = imageShape[0]
	height = imageShape[1]
	ero = numpy.array(ero, dtype=numpy.uint8)
	#ero = numpy.ones((5,3), dtype=numpy.uint8)
	#print(str(ero))
	widthERO, heightERO = ero.shape
	newImageArray = numpy.full((height, width), 255, dtype=numpy.uint8)
	#save_path = os.path.join(path, "result_morph", "resultadoErosao_dil=" + str(ero).replace('\n','') + "_" + img)
	for x in range(width):
		for y in range(height):
			if(imageArray[y, x] < 128): # should be == 0, but since the image isn't really binary, I have to do this
				willAppear = True
				for xx in range(widthERO):
					for yy in range(heightERO):
						if(ero[xx, yy] > 0):
							if(y + yy -center[1]< height and x + xx -center[0]< width):
								if(imageArray[yy+y-center[1], xx+x-center[0]] >= 128): # should be > 0, but since the image isn't really binary, I have to do this   
									willAppear = False
							else:
								willAppear = False
				if(willAppear):
					newImageArray[y, x] = 0
	#os.makedirs(os.path.dirname(save_path), exist_ok=True)
	#Image.fromarray(newImageArray).save(save_path)
	return newImageArray


def removeDots(img, bArray = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]):
	path = "Images"
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	cen = [1,1]
	save_path = os.path.join(path, "result_morph", "resultadoFinalMao2Dilatacoes_array=" + str(bArray).replace('\n','') + " center=" + str(cen).replace('\n','') + ".png")	
	imageErosion = erosion(imageArray, ero=bArray, center=cen)
	imageFinal = dilation(imageErosion, dil=bArray, center=cen)
	imageFinal2 = dilation(imageFinal, dil=bArray, center=cen)
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(imageFinal2).save(save_path)

def contorno(img, bArray = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]):
	#bArray = numpy.ones((3,5), dtype=numpy.uint8)
	#path = "Images"
	#im = Image.open(os.path.join(path, img), "r")
	#imageArray = numpy.array(im, dtype=numpy.uint8)
	#save_path = os.path.join(path, "result_morph", "resultadoContornoMao_array=" + str(bArray).replace('\n','') + ".png")
	imageShape = img.shape
	width = imageShape[0]
	height = imageShape[1]
	imageArrayBinary = numpy.full((height, width), 255, dtype=numpy.uint8)
	for x in range(width):
		for y in range(height):
			if(img[y, x] < 128):
				imageArrayBinary[y, x] = 0
			else:
				imageArrayBinary[y, x] = 255
	#print(imageArrayBinary)
	imageErosion = erosion(imageArrayBinary, bArray)
	#print(imageErosion)
	imageFinal = numpy.full((height, width), 255, dtype=numpy.uint8)
	for x in range(width):
		for y in range(height):
			imageValue = int(imageArrayBinary[y, x]) - int(imageErosion[y, x])
			#print(imageValue)
			if(imageValue < 0):
				imageFinal[y, x] = 0
			else:
				imageFinal[y, x] = 255
	#print(imageFinal)
	#os.makedirs(os.path.dirname(save_path), exist_ok=True)
	#Image.fromarray(imageFinal).save(save_path)
	return imageFinal


def blackAndWhite(img):
	#path = "Images"
	#im = Image.open(os.path.join(path, img), "r")
	#imageArray = numpy.array(im, dtype=numpy.uint8)
	#save_path = os.path.join(path, "result_morph", "resultadoB&W.png")
	imageShape = img.shape
	width = imageShape[0]
	height = imageShape[1]
	newImageArray = numpy.zeros((width, height), dtype=numpy.uint8)
	for x in range(width):
		for y in range(height):
			if(img[x, y] < 128):
				newImageArray[x, y] = 0
			else:
				newImageArray[x, y] = 255
	return newImageArray
	#print(newImageArray)
	#os.makedirs(os.path.dirname(save_path), exist_ok=True)
	#Image.fromarray(newImageArray).save(save_path)


def complement(img):
	imageShape = img.shape
	width = imageShape[1]
	height = imageShape[0]
	imgReturn = numpy.zeros((height, width), dtype=numpy.uint8)
	for xx in range(width):
		for yy in range(height):
			if(img[yy, xx] < 128):
				imgReturn[yy, xx] = 255
	return imgReturn

def matrixF(img, c=0):
	imageShape = img.shape
	width = imageShape[1]
	height = imageShape[0]
	if(c==0):
		imgReturn = numpy.full((height, width), 0, dtype=numpy.uint8)
		val = 255
	else:
		imgReturn = numpy.full((height, width), 255, dtype=numpy.uint8)
		val = 255
	for xx in range(width):
		value1 = val - int(img[0, xx])
		#print(value1)
		value2 = val - int(img[height-1, xx])
		imgReturn[0, xx] = abs(value1)
		#print(imgReturn[0, xx])
		imgReturn[height-1, xx] = abs(value2)
	for yy in range(height):
		value1 = val - int(img[yy, 0])
		value2 = val - int(img[yy, width-1])
		imgReturn[yy, 0] = abs(value1)
		imgReturn[yy, width-1] = abs(value2)
	return imgReturn

def intersection(img1, img2):
	imageShape = img1.shape
	width = imageShape[1]
	height = imageShape[0]
	imgReturn = numpy.full((height, width), 255, dtype=numpy.uint8)
	for xx in range(width):
		for yy in range(height):
			#value = img1[yy, xx] and img2[yy,xx]
			#if(value > 0):
			#	value = 255
			#imgReturn[yy, xx] = value
			if(img1[yy, xx] == 0 and img2[yy, xx] == 0):
				imgReturn[yy, xx] = 0
	return imgReturn

def preenchimento(img):
	path = "Images"
	im = Image.open(os.path.join(path, img), "r").convert('L')
	imageArray = numpy.array(im, dtype=numpy.uint8)
	#print(imageArray)
	imageShape = imageArray.shape
	width = imageShape[1]
	height = imageShape[0]
	save_path = os.path.join(path, "result_morph", "resultArray.png")
	save_path2 = os.path.join(path, "result_morph", "imageComplement.png")
	save_path3 = os.path.join(path, "result_morph", "imageF.png")
	save_path4 = os.path.join(path, "result_morph", "imageFDilated.png")
	save_path5 = os.path.join(path, "result_morph", "resultF.png")
	save_path6 = os.path.join(path, "result_morph", "finalResult.png")
	oldResultF = numpy.array(im, dtype=numpy.uint8)
	imageArray = blackAndWhite(imageArray) # make it binary
	imageArray = complement(imageArray)
	resultF = imageArray
	imageComplement = complement(resultF)
	dilationSize = numpy.full((3, 3), 1, dtype=numpy.uint8)
	imageF = matrixF(resultF, c=1)
	imageFDilated = dilation(imageF, dil=dilationSize, center=[1,1])
	resultF = intersection(imageFDilated, imageComplement)
	oldResultF = resultF
	timeToBreak = 0
	while(True):
		imageFDilated = dilation(resultF, dil=dilationSize, center=[1,1])
		resultF = intersection(imageFDilated, imageComplement)
		if(numpy.array_equal(oldResultF,resultF)):
			break
		oldResultF = resultF
		timeToBreak +=1
		if(timeToBreak >= 500):
			break
	print("Time to break = " + str(timeToBreak))
	resultArray = complement(resultF)
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(resultArray).save(save_path)
	os.makedirs(os.path.dirname(save_path2), exist_ok=True)
	Image.fromarray(imageComplement).save(save_path2)
	os.makedirs(os.path.dirname(save_path3), exist_ok=True)
	Image.fromarray(imageF).save(save_path3)
	os.makedirs(os.path.dirname(save_path4), exist_ok=True)
	Image.fromarray(imageFDilated).save(save_path4)
	os.makedirs(os.path.dirname(save_path5), exist_ok=True)
	Image.fromarray(resultF).save(save_path5)


begin = time.time()
removeDots("Image_(2a).jpg")
#contorno("maoDilatada.png")
#preenchimento("Image_(3a).jpg")
#preenchimento("letterA.png")
#contorno("Image_(3a).jpg")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
