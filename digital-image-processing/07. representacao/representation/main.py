import Image as im
import Segmentation as sg
import Representation as rp

def main():
    s = sg.Thresholding()
    r = rp.Representation()

    # ### questão 1
    img1 = s.otsu(im.Image("Image_(1).bmp"))
    img1 = r.chain(img1, directions=8)
    img1[0].save(extension="8_directions")

    ### questão 2
    img2 = s.otsu(im.Image("Image_(2).jpg"))
    img2 = r.chain(img2, directions=4, save=False, norm=False)
    r.mpp(img2[0], side=7)

if __name__ == '__main__':
    main()