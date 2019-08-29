import numpy as np
import Image as im
import Segmentation as seg

def main():
    ### questão 1
    e = seg.Edge()

    img = im.Image("Image_(1).jpg", noise=1, median=True, gauss=True)
    e_img = e.laplaceofGaussian(img, line=False)
    e_img.save(extension="edge")

    img = im.Image("Image_(1a).jpg", noise=2, median=True)
    e_img = e.laplaceofGaussian(img, line=False)
    e_img.save(extension="edge")

    img = im.Image("Image_(2a).jpg", noise=21, median=True, gauss=True)
    e_img = e.laplaceofGaussian(img, line=False)
    e_img.save(extension="edge_21x")

    ### questão 2
    s = seg.Thresholding()

    img = im.Image("Image_(3a).jpg", noise=2, median=True)  
    s_img = s.otsu(img)
    s_img.save(extension="thresholding")

    img = im.Image("Image_(3a).jpg", noise=5, gauss=True)  
    s_img = s.otsu(img, edge=True)
    s_img.save(extension="edge_thresholding")

    img = im.Image("Image_(3b).jpg", noise=3, median=True, gauss=True)  
    s_img = s.otsu(img)
    s_img.save(extension="thresholding")

    img = im.Image("Image_(3b).jpg", noise=41, median=True, gauss=True)  
    s_img = s.otsu(img, edge=True)
    s_img.save(extension="edge_thresholding")

    img1 = s.otsu(im.Image("Image_(3b).jpg", noise=41, median=True, gauss=True), edge=True)
    img2 = s.otsu(im.Image("Image_(3b).jpg", noise=3, median=True, gauss=True))
    img1.setImg(np.multiply(img1.arr, img2.arr))
    img1.save(extension="thresholding_mescle")

if __name__ == '__main__':
    main()