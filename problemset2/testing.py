from resizeable_image import *
from time import time

if __name__ == "__main__":
    images1 = [
        './images/5x5.png', 
        './images/10x10.png', 
        './images/20x10.png', 
        './images/12x12.png',
        './images/13x13.png',
        './images/14x14.png',
        './images/15x15.png']

    images2 = [
        './images/5x5.png',
        './images/10x10.png',
        './images/20x10.png',
        './images/12x12.png',
        './images/13x13.png',
        './images/14x14.png',
        './images/15x15.png',
        './images/20x20.png',
        './images/25x25.png',
        './images/50x50.png',
        './images/160x63.png',
        './images/195x210.png',
        './images/400x272.png',
        './images/400x400.png',
        './images/612x326.png',
        './images/640x253.png',
        './images/800x278.png']


    image_dict = {}
    for image in images1:
        start = time()
        img = ResizeableImage(image)
        seam = img.best_seam(False)
        end = time()
        print(f'{image} took {end-start} seconds to run')
        image = image.split('/')[-1]
        image = image.split('.')[0]
        image = image.replace('x', '*')
        image = str(eval(image))
        image_dict[image] = (end-start) * 1000
    f = open('naive_runtimes.txt', 'w')
    f.write(str(image_dict))
    f.close()

    image_dict2 = {}
    for image in images2:
        start = time()
        img = ResizeableImage(image)
        seam = img.best_seam(True)
        end = time()
        print(f'{image} took {end-start} seconds to run')
        image = image.split('/')[-1]
        image = image.split('.')[0]
        image = image.replace('x', '*')
        image = str(eval(image))
        image_dict2[image] = (end-start) * 1000
    
    f = open('dp_runtimes.txt', 'w')
    f.write(str(image_dict2))
    f.close()



