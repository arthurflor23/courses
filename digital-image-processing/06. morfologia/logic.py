from PIL import Image
import numpy
import math
import time
import os

def logicOperations(img1, img2):
	path = "Images"
	save_pathOR = os.path.join(path, "result_logicOperations", img1 + " OR " + img2)
	save_pathAND = os.path.join(path, "result_logicOperations", img1 + " AND " + img2)
	save_pathXOR = os.path.join(path, "result_logicOperations", img1 + " XOR " + img2)
	save_pathNAND = os.path.join(path, "result_logicOperations", img1 + " NAND " + img2)
	im1 = Image.open(os.path.join(path, img1), "r")
	imageArray1 = numpy.array(im1, dtype=numpy.uint8)
	im2 = Image.open(os.path.join(path, img2), "r")
	imageArray2 = numpy.array(im2, dtype=numpy.uint8)
	width, height = im1.size
	newImageArrayOR = numpy.zeros((height, width), dtype=numpy.uint8)
	newImageArrayAND = numpy.zeros((height, width), dtype=numpy.uint8)
	newImageArrayXOR = numpy.zeros((height, width), dtype=numpy.uint8)
	newImageArrayNAND = numpy.zeros((height, width), dtype=numpy.uint8)
	for xx in range(width):
		for yy in range(height):
			newImageArrayOR[yy, xx] = imageArray1[yy, xx, 0] or imageArray2[yy, xx, 0]
			newImageArrayAND[yy, xx] = imageArray1[yy, xx, 0] and imageArray2[yy, xx, 0]
			newImageArrayXOR[yy, xx] = (imageArray1[yy, xx, 0] and not imageArray2[yy, xx, 0]) or (not imageArray1[yy, xx, 0] and imageArray2[yy,xx, 0])
			newImageArrayNAND[yy, xx] = not newImageArrayAND[yy, xx]
			# not 0 will return 1, and we need it to be 255
			if newImageArrayNAND[yy, xx] > 0:
				newImageArrayNAND[yy, xx] = 255
			if newImageArrayXOR[yy, xx] > 0:
				newImageArrayXOR[yy, xx] = 255


	os.makedirs(os.path.dirname(save_pathOR), exist_ok=True)
	Image.fromarray(newImageArrayOR).save(save_pathOR)
	os.makedirs(os.path.dirname(save_pathAND), exist_ok=True)
	Image.fromarray(newImageArrayAND).save(save_pathAND)
	os.makedirs(os.path.dirname(save_pathXOR), exist_ok=True)
	Image.fromarray(newImageArrayXOR).save(save_pathXOR)
	os.makedirs(os.path.dirname(save_pathNAND), exist_ok=True)
	Image.fromarray(newImageArrayNAND).save(save_pathNAND)


begin = time.time()
logicOperations("Image_(1a).png", "Image_(1b).png")
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
