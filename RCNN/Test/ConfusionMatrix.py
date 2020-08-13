import os
import glob
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import models
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
from keras_video import VideoFrameGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, BatchNormalization, MaxPool2D, GlobalMaxPool2D, Flatten
from tensorflow.keras.layers import TimeDistributed, GRU, Dense, Dropout, LSTM

# use sub directories names as classes
classes = [i.split(os.path.sep)[1] for i in glob.glob('normal/*')]
classes.sort()
# some global params
SIZE = (150, 150)
CHANNELS = 3
NBFRAME = 5
#adapt bs size to sample size
BS = 234
# pattern to get videos and classes
glob_pattern='normal/{classname}/*.avi'

# for data augmentation
data_aug = keras.preprocessing.image.ImageDataGenerator(
    zoom_range=.1,
    horizontal_flip=True,
    rotation_range=8,
    width_shift_range=.2,
    height_shift_range=.2)

# Create video frame generator
train = VideoFrameGenerator(
    classes=classes, 
    glob_pattern=glob_pattern,
    nb_frames=NBFRAME,
    #split=0.5, 
    shuffle=False,
    batch_size=BS,
    target_shape=SIZE,
    nb_channel=CHANNELS,
    #transformation=none,
    use_frame_cache=True)

#Model is predicted
model= load_model('RCNNmodel.h5')
sample_test_images, labels = next(train)
label=[]
for iy in range(0,BS): 
    L = np.argmax(labels[iy])
    label.append(L)

prediction = model.predict(sample_test_images)
class_names = ['CI', 'PO']
pred=[]
for ix in range(0,BS): 
    P = np.argmax(prediction[ix])
    pred.append(P)
#confusion matrix is generated
mat = confusion_matrix(label, pred)
plot_confusion_matrix(conf_mat=mat, figsize=(6, 6), class_names = class_names, show_normed=False)
plt.show()
