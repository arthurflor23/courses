import numpy as np
import Image as im
import Segmentation as seg
import Morphology as mp

def main():
    s = seg.Thresholding()
    m = mp.Morphology()

    ### questão 1
    img1a = s.otsu(im.Image("Image_(1a).png"))
    img1b = s.otsu(im.Image("Image_(1b).png"))

    imgOR = m.logicalOperator(img1a, img1b, "OR")
    imgOR.save()

    imgAND = m.logicalOperator(img1a, img1b, "AND")
    imgAND.save()

    imgXOR = m.logicalOperator(img1a, img1b, "XOR")
    imgXOR.save()

    imgNAND = m.logicalOperator(img1a, img1b, "NAND")
    imgNAND.save()


    ## questão 2
    img2a = s.otsu(im.Image("Image_(2a).jpg"))
    d_img2a = m.erode(m.erode(m.dilate(img2a)))
    d_img2a.save()


    ### questão 3
    img3a = s.otsu(im.Image("Image_(3a).jpg"))

    d_img3a = m.floodFill(img3a, (0,0), 1)
    d_img3a.save(extension="floodFill")

    d_img3a.setImg(np.logical_not(d_img3a.arr))
    d_img3a.save(extension="floodFill_inverse")

    img = m.logicalOperator(img3a, d_img3a, "OR")
    img.save(extension="floodFill")


    ### questão 4
    img4a = s.otsu(im.Image("Image_(4a).jpg"))

    d_img4a = m.floodFill(img4a, (0,0), 1)
    d_img4a = m.dilate(d_img4a)
    d_img4a.setImg(np.logical_not(d_img4a.arr))

    img = m.logicalOperator(img4a, d_img4a, "OR")
    img = m.skeleton(img)

    img.save(extension="skeleton")


if __name__ == '__main__':
    main()