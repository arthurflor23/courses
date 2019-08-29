import Image as im

def main():

    img = im.Image("Image_(1a)", type="jpg")
    img.light(h=1, s=2, i=10)
    img.save(extension="hsv_lighten")

    img = im.Image("Image_(1b)", type="jpg")
    img.light(h=1, s=1.5, i=0.4)
    img.save(extension="hsv_darken_2")

    img = im.Image("Image_(2b)", type="jpg")
    extension = img.clear(times=7, side=3, factor="rgb", median=True)
    img.save(extension=extension)

if __name__ == '__main__':
    main()