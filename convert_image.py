# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 12:31:55 2017

@author: ITRI-A50117
"""

import os
from shutil import copyfile
from PIL import Image
from PIL import ImageFile

# https://stackoverflow.com/questions/12984426/python-pil-ioerror-image-file-truncated-with-big-images
ImageFile.LOAD_TRUNCATED_IMAGES = True

if __name__ == '__main__':
    
    album_path = 'C:/album/kwbuster'
    convert_path = os.path.join(os.path.dirname(__file__),'images')
    
    image_dirs = [x[1] for x in os.walk(album_path)][0]
    for image_dir in image_dirs:
        if not os.path.exists(convert_path + '/' + image_dir):
            os.makedirs(convert_path + '/' + image_dir)
        
        files = [x[2] for x in os.walk(album_path + '/' + image_dir)][0]
        for file in files:
            if not file.endswith('.jpg'):
                im = Image.open(album_path + '/' + image_dir + '/' + file)
                im.convert('RGB').save(convert_path + '/' + image_dir + '/%s.jpg' %(file[:-4]))
            else:
                copyfile(album_path + '/' + image_dir + '/' + file, convert_path + '/' + image_dir + '/' + file)