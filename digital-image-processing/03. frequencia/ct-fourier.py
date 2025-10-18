from PIL import Image
import numpy
import math
import os

### Cooley-Tukey Fast Fourier Transform ###
def fft(x):
    n = len(x)
    if (n == 1):
        return x
    f_even, f_odd = fft(x[0::2]), fft(x[1::2])
    s = [0] * n
    for m in range(n//2):
        omega = numpy.exp((-2j * numpy.pi * m) / n)
        s[m] = f_even[m] + omega * f_odd[m]
        s[m + n//2] = f_even[m] - omega * f_odd[m]
    return s

def pad2(x):
   m, n = numpy.shape(x)
   M, N = 2 ** int(math.ceil(math.log(m, 2))), 2 ** int(math.ceil(math.log(n, 2)))
   F = numpy.zeros((M,N), dtype=x.dtype)
   F[0:m, 0:n] = x
   return F, m, n

def fft2(f):
   f, m, n = pad2(f)
   return numpy.transpose(fft(numpy.transpose(fft(f)))), m, n

def ifft2(F, m, n):
    f, M, N = fft2(numpy.conj(F))
    f = numpy.matrix(numpy.real(numpy.conj(f)))/(M*N)
    return f[0:m, 0:n]

def fourier(img):
    arr = openImg(img)

    f, m, n = fft2(arr)
    saveImg(img, numpy.abs(f), "frequence")

    f = applyFilter(f)
    # saveImg(img, numpy.abs(f), "laplace")

    i = ifft2(f, m, n)
    # saveImg(img, numpy.real(i), "invert")
    saveImg(img, numpy.add(arr, numpy.real(i)), "invert")


### Utils ###
def applyFilter(arr):
    h, w = numpy.shape(arr)
    P = (2*h + 1)
    Q = (2*w + 1)
    Dzero = 320
    n = 2

    for v in range(h):
        for u in range(w):
            D = math.sqrt((((u - (P/2))**2) + (((v - (Q/2))**2))))

            # H[v,u] = (1 / (1 + ((D0 / D)**(2*n))))                ## butterworth
            # H[v,u] = (1 - numpy.exp(-(D**2) / (2*(D0**2))))         ## gaussiano
            # H[v,u] = (-4 * (numpy.pi**2) * ((u**2) + (v**2)))     ## laplaciano

            arr[v,u] = (arr[v,u] * (1 - numpy.exp(-(D**2) / (2*(Dzero**2)))))
    return arr

def openImg(img):
    return numpy.array(Image.open(img, "r"), dtype=numpy.float64)

def saveImg(img, n_arr, extension=""):
    os.makedirs(os.path.dirname(img), exist_ok=True)
    # Image.fromarray(n_arr).convert("L").show()
    Image.fromarray(n_arr).convert("L").save(img.replace(".", ("_" + extension + ".")))

### Main ###
def main():
    img = [
        "Agucar_(0).jpg",
        # "Agucar_(1).jpg",
        # "Agucar_(2).jpg",
        # "Agucar_(3).jpg",
        # "Agucar_(4).jpg",
        # "Agucar_(5).jpg",
    ]
    for x in range(len(img)):
        fourier(os.path.join("images", img[x]))

if __name__ == "__main__":
    main()