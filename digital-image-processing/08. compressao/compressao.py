from PIL import Image
from pathlib import Path
import numpy
import math
import time
import os


def RLEDecode(rleArray):
	size = rleArray.size
	arrayLine = []
	arrayTotal = []
	value = True # start as white
	for i in range(size):
		if(rleArray[i] < 255): # 255 = new line
			for v in range(rleArray[i]):
				arrayLine.append(value)
			value = not value
		else: #if it's a new line
			arrayTotal.append((arrayLine))
			arrayLine = []
			value = not value
	arrayTotal.append((arrayLine)) # last line doesn't have a 255 on the end
	width = len(arrayTotal[0])
	height = len(arrayTotal)
	newArray = numpy.zeros((height, width), dtype=numpy.uint8)
	for yy in range(height):
		for xx in range(width):
			newArray[yy, xx] = int(arrayTotal[yy][xx])
	return newArray


def RLE(binArray):
	height, width = binArray.shape
	arrayCount = []
	count = 0
	valueToCheck = 1 # start as white
	#255 = linebreak
	#goes only from values 0 to 254
	for yy in range(height):
		for xx in range(width):
			if(valueToCheck == binArray[yy,xx]):
				if(count == 254): #max value
					arrayCount.append(count)
					count = 0
					arrayCount.append(count)
				count+=1
			else:
				arrayCount.append(count)
				count = 1
				valueToCheck = binArray[yy, xx]
		arrayCount.append(count)
		if(yy < height-1):
			arrayCount.append(255) #new line
			count = 0
	arrayCount = numpy.array(arrayCount, dtype = numpy.uint8)
	return arrayCount

def binaryBitplan(img):
	path = "data"
	filesPath = Path("out/files/" + img[:-4] + "/")
	im = Image.open(os.path.join(path, img), "r")
	imageArray = numpy.array(im, dtype=numpy.uint8)
	if(len(imageArray.shape) == 3):
		imageArray = imageArray[:, :, 0]
	width, height = im.size
	a7 = numpy.zeros((height, width), dtype=numpy.bool)
	a6 = numpy.zeros((height, width), dtype=numpy.bool)
	a5 = numpy.zeros((height, width), dtype=numpy.bool)
	a4 = numpy.zeros((height, width), dtype=numpy.bool)
	a3 = numpy.zeros((height, width), dtype=numpy.bool)
	a2 = numpy.zeros((height, width), dtype=numpy.bool)
	a1 = numpy.zeros((height, width), dtype=numpy.bool)
	a0 = numpy.zeros((height, width), dtype=numpy.bool)
	g7 = numpy.zeros((height, width), dtype=numpy.bool)
	g6 = numpy.zeros((height, width), dtype=numpy.bool)
	g5 = numpy.zeros((height, width), dtype=numpy.bool)
	g4 = numpy.zeros((height, width), dtype=numpy.bool)
	g3 = numpy.zeros((height, width), dtype=numpy.bool)
	g2 = numpy.zeros((height, width), dtype=numpy.bool)
	g1 = numpy.zeros((height, width), dtype=numpy.bool)
	g0 = numpy.zeros((height, width), dtype=numpy.bool)
	for yy in range(height):
		for xx in range(width):
			valueBin = bin(imageArray[yy, xx])[2:].zfill(8)
			a0[yy, xx] = bool(int(valueBin[7]))
			a1[yy, xx] = bool(int(valueBin[6]))
			a2[yy, xx] = bool(int(valueBin[5]))
			a3[yy, xx] = bool(int(valueBin[4]))
			a4[yy, xx] = bool(int(valueBin[3]))
			a5[yy, xx] = bool(int(valueBin[2]))
			a6[yy, xx] = bool(int(valueBin[1]))
			a7[yy, xx] = bool(int(valueBin[0]))	

			g7[yy, xx] = a7[yy, xx]
			g6[yy, xx] = XOR(a6[yy, xx], a7[yy, xx])
			g5[yy, xx] = XOR(a5[yy, xx], a6[yy, xx])
			g4[yy, xx] = XOR(a4[yy, xx], a5[yy, xx])
			g3[yy, xx] = XOR(a3[yy, xx], a4[yy, xx])
			g2[yy, xx] = XOR(a2[yy, xx], a3[yy, xx])
			g1[yy, xx] = XOR(a1[yy, xx], a2[yy, xx])
			g0[yy, xx] = XOR(a0[yy, xx], a1[yy, xx])

	a0RLE = RLE(a0)
	a1RLE = RLE(a1)
	a2RLE = RLE(a2)
	a3RLE = RLE(a3)
	a4RLE = RLE(a4)
	a5RLE = RLE(a5)
	a6RLE = RLE(a6)
	a7RLE = RLE(a7)

	g0RLE = RLE(g0)
	g1RLE = RLE(g1)
	g2RLE = RLE(g2)
	g3RLE = RLE(g3)
	g4RLE = RLE(g4)
	g5RLE = RLE(g5)
	g6RLE = RLE(g6)
	g7RLE = RLE(g7)
	

	os.makedirs(filesPath, exist_ok=True)
	numpy.save(filesPath / "g0.npy", g0)
	numpy.save(filesPath / "g0RLE.npy", g0RLE)
	numpy.save(filesPath / "g1.npy", g1)
	numpy.save(filesPath / "g1RLE.npy", g1RLE)
	numpy.save(filesPath / "g2.npy", g2)
	numpy.save(filesPath / "g2RLE.npy", g2RLE)
	numpy.save(filesPath / "g3.npy", g3)
	numpy.save(filesPath / "g3RLE.npy", g3RLE)
	numpy.save(filesPath / "g4.npy", g4)
	numpy.save(filesPath / "g4RLE.npy", g4RLE)
	numpy.save(filesPath / "g5.npy", g5)
	numpy.save(filesPath / "g5RLE.npy", g5RLE)
	numpy.save(filesPath / "g6.npy", g6)
	numpy.save(filesPath / "g6RLE.npy", g6RLE)
	numpy.save(filesPath / "g7.npy", g7)
	numpy.save(filesPath / "g7RLE.npy", g7RLE)

	numpy.save(filesPath / "a0.npy", a0)
	numpy.save(filesPath / "a0RLE.npy", a0RLE)
	numpy.save(filesPath / "a1.npy", a1)
	numpy.save(filesPath / "a1RLE.npy", a1RLE)
	numpy.save(filesPath / "a2.npy", a2)
	numpy.save(filesPath / "a2RLE.npy", a2RLE)
	numpy.save(filesPath / "a3.npy", a3)
	numpy.save(filesPath / "a3RLE.npy", a3RLE)
	numpy.save(filesPath / "a4.npy", a4)
	numpy.save(filesPath / "a4RLE.npy", a4RLE)
	numpy.save(filesPath / "a5.npy", a5)
	numpy.save(filesPath / "a5RLE.npy", a5RLE)
	numpy.save(filesPath / "a6.npy", a6)
	numpy.save(filesPath / "a6RLE.npy", a6RLE)
	numpy.save(filesPath / "a7.npy", a7)
	numpy.save(filesPath / "a7RLE.npy", a7RLE)

def decodeImageBinary(imgName, decode=True):
	filesPath = Path("out/files/" + imgName + "/")
	savePath = Path("out/resultBinary/" + imgName + "/")
	if(decode):
		a7 = RLEDecode(numpy.load(filesPath / "a7RLE.npy"))
		a6 = RLEDecode(numpy.load(filesPath / "a6RLE.npy"))
		a5 = RLEDecode(numpy.load(filesPath / "a5RLE.npy"))
		a4 = RLEDecode(numpy.load(filesPath / "a4RLE.npy"))
		a3 = RLEDecode(numpy.load(filesPath / "a3RLE.npy"))
		a2 = RLEDecode(numpy.load(filesPath / "a2RLE.npy"))
		a1 = RLEDecode(numpy.load(filesPath / "a1RLE.npy"))
		a0 = RLEDecode(numpy.load(filesPath / "a0RLE.npy"))
	else:
		a7 = numpy.load(filesPath / "a7.npy")
		a6 = numpy.load(filesPath / "a6.npy")
		a5 = numpy.load(filesPath / "a5.npy")
		a4 = numpy.load(filesPath / "a4.npy")
		a3 = numpy.load(filesPath / "a3.npy")
		a2 = numpy.load(filesPath / "a2.npy")
		a1 = numpy.load(filesPath / "a1.npy")
		a0 = numpy.load(filesPath / "a0.npy")
	height, width = a7.shape
	newImageArray = numpy.zeros((height, width), dtype=numpy.uint8)
	save_path = os.path.join(savePath, imgName + "_without3Bits.png")
	for yy in range(height):
		for xx in range(width):
			newImageArray[yy, xx] = (a7[yy, xx] * 128) + (a6[yy, xx] * 64) + (a5[yy, xx] * 32) + (a4[yy,xx] * 16) + (a3[yy, xx] * 8) # + (a2[yy, xx] * 4) + (a1[yy, xx] * 2) + (a0[yy, xx])
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)

	a0[a0 > 0] = 255
	a1[a1 > 0] = 255
	a2[a2 > 0] = 255
	a3[a3 > 0] = 255
	a4[a4 > 0] = 255
	a5[a5 > 0] = 255
	a6[a6 > 0] = 255
	a7[a7 > 0] = 255
	Image.fromarray(a7).save(savePath / "a7.png")
	Image.fromarray(a6).save(savePath / "a6.png")
	Image.fromarray(a5).save(savePath / "a5.png")
	Image.fromarray(a4).save(savePath / "a4.png")
	Image.fromarray(a3).save(savePath / "a3.png")
	Image.fromarray(a2).save(savePath / "a2.png")
	Image.fromarray(a1).save(savePath / "a1.png")
	Image.fromarray(a0).save(savePath / "a0.png")


def decodeImageGray(imgName, decode=True):
	filesPath = Path("out/files/" + imgName + "/")
	savePath = Path("out/resultGray/" + imgName + "/")
	if(decode):
		g7 = RLEDecode(numpy.load(filesPath / "g7RLE.npy"))
		g6 = RLEDecode(numpy.load(filesPath / "g6RLE.npy"))
		g5 = RLEDecode(numpy.load(filesPath / "g5RLE.npy"))
		g4 = RLEDecode(numpy.load(filesPath / "g4RLE.npy"))
		g3 = RLEDecode(numpy.load(filesPath / "g3RLE.npy"))
		g2 = RLEDecode(numpy.load(filesPath / "g2RLE.npy"))
		g1 = RLEDecode(numpy.load(filesPath / "g1RLE.npy"))
		g0 = RLEDecode(numpy.load(filesPath / "g0RLE.npy"))
	else:
		g7 = numpy.load(filesPath / "g7.npy")
		g6 = numpy.load(filesPath / "g6.npy")
		g5 = numpy.load(filesPath / "g5.npy")
		g4 = numpy.load(filesPath / "g4.npy")
		g3 = numpy.load(filesPath / "g3.npy")
		g2 = numpy.load(filesPath / "g2.npy")
		g1 = numpy.load(filesPath / "g1.npy")
		g0 = numpy.load(filesPath / "g0.npy")
	height, width = g7.shape
	newImageArray = decodeGrayCode(height, width, g7, g6, g5, g4, g3, g2, g1, g0)
	save_path = os.path.join(savePath, imgName + "_without3Bits.png")
	os.makedirs(os.path.dirname(save_path), exist_ok=True)
	Image.fromarray(newImageArray).save(save_path)
	
	g0[g0 > 0] = 255
	g1[g1 > 0] = 255
	g2[g2 > 0] = 255
	g3[g3 > 0] = 255
	g4[g4 > 0] = 255
	g5[g5 > 0] = 255
	g6[g6 > 0] = 255
	g7[g7 > 0] = 255
	Image.fromarray(g7).save(savePath / "g7.png")
	Image.fromarray(g6).save(savePath / "g6.png")
	Image.fromarray(g5).save(savePath / "g5.png")
	Image.fromarray(g4).save(savePath / "g4.png")
	Image.fromarray(g3).save(savePath / "g3.png")
	Image.fromarray(g2).save(savePath / "g2.png")
	Image.fromarray(g1).save(savePath / "g1.png")
	Image.fromarray(g0).save(savePath / "g0.png")
	

def XOR(arg1, arg2):
	ret = not(arg1 and arg2) and (arg1 or arg2)
	return ret


def decodeGrayCode(height, width, g7, g6, g5, g4, g3, g2, g1, g0):
	newImageArray2 = numpy.zeros((height, width), dtype=numpy.uint8)
	for yy in range(height):
		for xx in range(width):
			a7 = g7[yy, xx]
			a6 = XOR(g6[yy, xx], a7)
			a5 = XOR(g5[yy, xx], a6)
			a4 = XOR(g4[yy, xx], a5)
			a3 = XOR(g3[yy, xx], a4)
			a2 = XOR(g2[yy, xx], a3)
			a1 = XOR(g1[yy, xx], a2)
			a0 = XOR(g0[yy, xx], a1)
			newImageArray2[yy, xx] = (a7 * 128) + (a6 * 64) + (a5 * 32) + (a4 * 16) + (a3 * 8)# + (a2 * 4) + (a1 * 2) + a0
	return newImageArray2


begin = time.time()
binaryBitplan("Image_(3).tif")
decodeImageBinary("Image_(3)")
decodeImageGray("Image_(3)")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
