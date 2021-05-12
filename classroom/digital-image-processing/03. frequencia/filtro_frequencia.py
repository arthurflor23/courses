from PIL import Image
import numpy
import math
import cmath
import time
import os

numpy.set_printoptions(threshold=numpy.nan)

#M = size of the array, must be a power of 2 or it breaks I guess
#Don't seem to be working as intended
def FFT(array1D, invert):
        M = len(array1D)
        if M==1:
                return array1D
        else:
                evenArray1D = FFT(array1D[::2], invert)
                oddArray1D = FFT(array1D[1::2], invert)
                #print("M = " + str(M))
                for i in range(M//2):
                        k = i + M//2
                        tempValue = array1D[i]
                        #cosSenAtt = (2 * math.pi * i)/M
                        #cos = math.cos(cosSenAtt)
                        #sin = math.sin(cosSenAtt)
                        #exponential = cos - 1j*sin
                        if(invert):
                                exponential = cmath.exp((2 * math.pi * i * 1j)/M)
                        else:
                                exponential = cmath.exp((-2 * math.pi * i * 1j)/M)
                        #print("Somando: ")
                        #print(tempValue + exponential * array1D[k])
                        array1D[i] = tempValue + exponential * array1D[k]
                        #print("Dentro do array: ")
                        #print(array1D[i])
                        array1D[k] = tempValue - exponential * array1D[k]
                return array1D



# Working!
def DFT(array1D, invert):
        M = len(array1D)
        #print("Array 1D Lenght: " + str(M))
        multiplier = 1/(math.sqrt(M))
        #numReal = []
        #numImaginary = []
        numComplete = []
        for m in range(M):
                sumReal = 0
                sumImaginary = 0
                for u in range(M):
                        cosSenAtt = 2 * math.pi * ((m * u)/M)
                        cos = math.cos(cosSenAtt)
                        sin = math.sin(cosSenAtt)
                        if(invert):
                                sin = -sin
                        sumReal += array1D[u] * cos
                        sumImaginary += array1D[u] * -1j * sin
                sumReal *= multiplier
                sumImaginary *= multiplier
                #numReal.append(sumReal)
                #numImaginary.append(sumImaginary)
                #numComplete.append(int(round(numpy.abs(sumReal + sumImaginary))))
                numComplete.append(sumReal + sumImaginary)
        return numComplete

#Working!
def DFT2D(array2D, invert):
        M = len(array2D)
        N = len(array2D[0])
        #print("Lines: " + str(M))
        #print("Columns: " + str(N))
        firstMatrix = []
        secondMatrix = []

        
        for row in range(M):
                tempRow = []
                for col in range(N):
                        tempRow.append(array2D[row][col])
                newRow = DFT(tempRow, invert)
                firstMatrix.append(newRow)
        for col in range(N):
                tempCol = []
                for row in range(M):
                        tempCol.append(firstMatrix[row][col])
                newCol = DFT(tempCol, invert)
                secondMatrix.append(newCol)
        secondMatrix = list(map(list, zip(*secondMatrix)))
        return secondMatrix


def filter(img):
        path = "images"
        save_path = os.path.join(path, "result_frequencia", "resultado_" + img)
        im = Image.open(os.path.join(path, img), "r")
        imageArray = numpy.array(im, dtype=numpy.uint8)
        #print("Imagem Sem Filtro: ")
        #print(imageArray)
        print("Entrou no DFT2D")
        newImage = DFT2D(imageArray, False)
        #print("Imagem Com Filtro: ")
        #print(newImage)

        n = 2
        d0 = 80
        print("Entrou no Filtro")
        #newImage = gaussianFilter(newImage, n, d0)
        newImage = butterworthFilter(newImage, n, d0)
        
        print("Entrou no DFT2D Inverso")
        newImageInverted = DFT2D(newImage, True)
        #print("Imagem Sem Filtro Invertida: ")
        #print(newImageInverted)
        #width, height = im.size
        newImageInverted = numpy.array(newImageInverted)
        newImageInverted = numpy.round(numpy.abs(newImageInverted))
        newImageInverted = newImageInverted.astype(numpy.uint8)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        Image.fromarray(newImageInverted).save(save_path)


#not working as it should, at least it doesn't looks like it
def butterworthFilter(img, n, d0):
        rows = len(img)
        cols = len(img[0])
        print("Rows: " + str(rows))
        print("Cols: " + str(cols))
        img = numpy.array(img)
        filteredImage = numpy.zeros((rows, cols, 3), dtype=complex)
        for x in range(rows):
                for y in range(cols):
                        #D = math.sqrt(rows**2 + cols**2)
                        D = math.sqrt( ((x - (rows/2))**2) + ((y - (cols/2))**2) )
                        H = 1/(1+ 0.414*((d0/D)**(2*n)))
                        filteredImage[x, y] = img[x, y] * H
        return filteredImage

# can't see any difference from the butterworth one
def gaussianFilter(img, n, d0):
        rows = len(img)
        cols = len(img[0])
        print("Rows: " + str(rows))
        print("Cols: " + str(cols))
        img = numpy.array(img)
        filteredImage = numpy.zeros((rows, cols, 3), dtype=complex)
        for x in range(rows):
                for y in range(cols):
                        #D = math.sqrt(rows**2 + cols**2)
                        D = math.sqrt( ((x - (rows/2))**2) + ((y - (cols/2))**2) )
                        DD = D*D
                        H = 1 - math.exp(-DD/(2 * d0 * d0))
                        filteredImage[x, y] = img[x, y] * H
        return filteredImage

#testArray = [1, 3, 5, 7, 9, 8, 6, 4]
#testArray = [1.0, 2.0, 1.0, -1.0, 1.5]
testArrayLivro = [1.0, 3.0, 5.0, 7.0, 9.0, 8.0, 6.0, 4.0, 2.0, 0.0]
testArrayInternet = [0, 0, 2, 3, 4, 0, 0, 0]
testMatrix = [[5, 3, 0, 2], [1, 7, 8, 3], [4, 2, 2, 2], [8, 5, 2, 1]]
test2Matrix = [[0,0,0,0,0,0,0,0], [0,0,70,80,90,0,0,0],[0,0,90,100,110,0,0,0],[0,0,110,120,130,0,0,0],[0,0,130,140,150,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

#print("Test 2D FFT Numpy: ")
#print(numpy.fft.fft(test2Matrix))

#print("Original Array: ")
#print(testArrayInternet)
#print("With Numpy FFT: ")
#print(numpy.fft.fft(testArrayInternet))
#print("With the Inverse FFT: ")
#print(numpy.fft.ifft(numpy.fft.fft(testArray)))
#numpy.set_printoptions(suppress=True)

#print("With DFT: ")
#print(numpy.array(DFT(testArrayInternet, False)))
#print("With DFT Inverse: ")
#print(numpy.array(DFT(DFT(testArray, False), True)))
#print("With my FFT: ")
#myFFT = FFT(testArrayInternet, False)
#print(myFFT)

#print("Original Matrix: ")
#print(numpy.matrix(test2Matrix))
#print("2D DFT Test: ")
#test2D = DFT2D(test2Matrix, False)
#print(numpy.matrix(test2D))
#print("2D DFT Invert Test: ")
#test2DInvert = DFT2D(test2D,True)
#test2DInvert = numpy.array(test2DInvert)
#test2DInvert = numpy.round(numpy.abs(test2DInvert))
#test2DInvert = test2DInvert.astype(int)
#print(numpy.matrix(test2DInvert))

begin = time.time()
filter("Agucar_(1).jpg")
#filter("Agucar_(2).jpg") # only try this if you are using a super computer from NASA
end = time.time()

print("Finalizado: " + str(round(end-begin, 2)) + "s\n")
