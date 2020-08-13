import tensorflow as tf
import tensorflow_addons as tfa
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import glob 


# Before running convert tif images to png images

tf.compat.v1.enable_eager_execution()
def rot(filename, dirpath, k):
    os.chdir(path)
    filename=str(filename)
    image_string=tf.compat.v1.read_file(filename)
    image = tf.image.decode_png(image_string,channels=3)
    a=k*np.pi/180
    rot_tensor = tfa.image.rotate(image, angles=a) 
    rot_png = tf.image.encode_png(rot_tensor)
    file_name = tf.constant('rot'+ str(k) + filename)
    file = tf.compat.v1.write_file(file_name, rot_png)

def fliplr(filename, path):
    os.chdir(path)
    filename=str(filename)
    image_string=tf.compat.v1.read_file(filename)
    image = tf.image.decode_png(image_string,channels=3)
    lr_tensor = tf.image.flip_left_right(image)
    lr_png = tf.image.encode_png(lr_tensor)
    file_name = tf.constant('lr' + filename)
    file = tf.compat.v1.write_file(file_name, lr_png)

def flipud(filename,path):
    os.chdir(path)
    filename=str(filename)
    image_string=tf.compat.v1.read_file(filename)
    image = tf.image.decode_png(image_string,channels=3)
    ud_tensor = tf.image.flip_up_down(image)
    ud_png = tf.image.encode_png(ud_tensor)
    file_name = tf.constant('ud' + filename)
    file = tf.compat.v1.write_file(file_name, ud_png)

#Path to the images
path='C:/TW565le/Uebergabe_test/images/PO'
dirs=os.listdir(path)

for i in range(0, len(dirs)):
    dirpath= path + os.sep + str(dirs[i])
    print('d', dirs[i])
    fliplr(dirs[i], path)
    flipud(dirs[i], path)
    k=1
    alpha=0
    # adapt k and alpha
    while k < 10:
        alpha=alpha + 35
        rot(dirs[i], path, alpha)
        k=k+1
