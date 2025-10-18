from PIL import Image
from matplotlib import pyplot as plot
import numpy as np
import os

### Fast Fourier Transform ###
def fft(arr, type=None):
    M, N = np.shape(arr)

    x = np.arange(M, dtype=float)
    y = np.arange(N, dtype=float)

    u = x.reshape((M,1))
    v = y.reshape((N,1))

    div, j = 1, 2j
    if (type is None):
        div, j = (M*N), -2j
    
    exp_1 = np.exp(j * np.pi * u * (x/M))
    exp_2 = np.exp(j * np.pi * v * (y/N))

    F = (np.dot(exp_2, np.dot(exp_1, arr).transpose()) / div)
    return F

def prepare(arr) :
    M, N = np.shape(arr)
    m, n = (M//2), (N//2)

    n_arr = np.zeros((M,N))
    n_arr[-m:,-n:] = np.abs(arr[:m,:n])
    n_arr[-m:,:-n] = np.abs(arr[:m,n:])
    n_arr[:-m,-n:] = np.abs(arr[m:,:n])
    n_arr[:-m,:-n] = np.abs(arr[m:,n:])

    return np.transpose(np.log(n_arr**2))

def getFilter(arr):
    h, w = np.shape(arr)
    H = np.zeros((h, w), arr.dtype)
    Dzero = 60

    for v in range(h):
        for u in range(w):
            D = np.sqrt((((u - (w/2))**2) + (((v - (h/2))**2))))

            # H[v,u] = (1 / (1 + ((Dzero / D)**(2*2))))          ## butterworth
            # H[v,u] = (1 - np.exp(-(D**2) / (2*(Dzero**2))))    ## gaussiano
            # H[v,u] = (-4 * (np.pi**2) * ((u**2) + (v**2)))
            
            H[v,u] = (1 - np.exp(-(D**2) / (2*(Dzero**2))))
    return H

def fourier(img_name):
    arr = readImg(img_name)

    F = fft(arr)
    # saveImg(img_name, prepare(F), "r_frequency")
    # showImg(prepare(F))

    H = getFilter(F)
    # saveImg(img_name, np.abs(H), "r_frequency_filter")
    # showImg(prepare(f))

    f = np.multiply(F, H)

    i = np.abs(fft(f, "i"))
    # showImg(i)

    return i

### Utils ###
def showImg(F, mode="Greys_r"):
    # Image.fromarray(F).convert("L").show()
    plot.imshow(F, cmap=mode)
    plot.show()

def readImg(img, path="images"):
    return np.array(Image.open(os.path.join(path, img), "r"), dtype=np.float64)

def saveImg(img_name, img_array=None, extension=None, path="images", mode="Greys_r"):
    if (not img_array is None):
        os.makedirs(path, exist_ok=True)
        plot.imsave(os.path.join(path, img_name.replace(".", ("_" + extension + "."))), img_array, cmap=mode)

### Main ###
def main():
    img = [
        # "Agucar_(0).jpg",
        "Agucar_(1).jpg",
        "Agucar_(2).jpg",
        "Agucar_(3).jpg",
        "Agucar_(4).jpg",
        "Agucar_(5).jpg",
    ]
    for x in range(len(img)):
        saveImg(img[x], fourier(img[x]), "result")

if __name__ == "__main__":
    main()