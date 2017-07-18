""" Convert All Files in PIXNET Album into .JPG Format
# Description:
    After downloading all the pictures in PIXNET album, we need to get rid of generated numbers and convert the formate for smaller storage capacity.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/18
# Reference:
    - https://sofree.cc/bloginwp-pixnet-album/
    - http://laby2.blogspot.com/
    - http://pillow.readthedocs.io/en/3.0.x/handbook/image-file-formats.html
"""
import os
from shutil import copyfile
from PIL import Image
from PIL import ImageFile

# Avoid "image truncated: error
# https://stackoverflow.com/questions/12984426/python-pil-ioerror-image-file-truncated-with-big-images
ImageFile.LOAD_TRUNCATED_IMAGES = True

if __name__ == '__main__':

    # PIXNET album path
    album_path = 'path/to/album'
    # path of converted album
    convert_path = os.path.join(os.path.dirname(__file__),'images')

    # search for sub-albums in the album_path
    image_dirs = [x[1] for x in os.walk(album_path)][0]
    for image_dir in image_dirs:
        ind = image_dir.index('-') + 1

        if not os.path.exists(convert_path + '/' + image_dir[8:]):
            os.makedirs(convert_path + '/' + image_dir[ind:])

        # search for files in the album_path
        files = [x[2] for x in os.walk(album_path + '/' + image_dir)][0]
        for file in files:
            idx = file.index('-') + 1

            # image convertion
            if not file.endswith('.jpg'):
                im = Image.open(album_path + '/' + image_dir + '/' + file)
                im.convert('RGB').save(convert_path + '/' + image_dir[ind:] + '/%s.jpg' %(file[idx:-4]))
            else:
                copyfile(album_path + '/' + image_dir + '/' + file, convert_path + '/' + image_dir[ind:] + '/' + file[idx:])
