# -*- coding: utf-8 -*-
import os
from shutil import rmtree, copyfile
from PIL import Image
import math

if __name__ == "__main__":
    
    source_dir = "../KodeWorker.github.io/assets/images"    
    target_dir = "images"
    limit = 1024
    quality = 98
    
    if os.path.exists(target_dir):
        rmtree(target_dir)
    os.makedirs(target_dir)
    
    for dirPath, dirNames, fileNames in os.walk(source_dir):
        for fileName in fileNames:
            if fileName.lower().endswith(".jpg") or\
            fileName.lower().endswith(".png"):
            
                source_path = os.path.join(dirPath, fileName)
                dirname = os.path.dirname(source_path)
                dirname = dirname.replace(source_dir, target_dir)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                target_path = os.path.join(dirname, fileName)
                
                # Image Compression                
                img = Image.open(source_path)
                if max(img.size) > limit:
                    h = img.size[0]
                    w = img.size[1]
                    if h >= w:
                        ratio = limit/h
                    else:
                        ratio = limit/w
                    size = math.ceil(h*ratio), math.ceil(w*ratio)
                    
                    img.thumbnail(size, Image.ANTIALIAS)
                img.save(target_path, optimize=True, quality=quality)
            
            elif fileName.lower().endswith(".gif"):
                
                source_path = os.path.join(dirPath, fileName)
                dirname = os.path.dirname(source_path)
                dirname = dirname.replace(source_dir, target_dir)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                target_path = os.path.join(dirname, fileName)
                
                copyfile(source_path, target_path)