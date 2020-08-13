from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt

from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix


#Test images have to be in CI,PO and HC folders
#There must be at least one image in each folder

#Name of the CNN model
model= load_model('all_Alexnet_model.h5')


#path to the test images
test_dir = 'F:/DataCNN/Test/confusion/4/70'
batch_size = 200 #same number as data available
IMG_HEIGHT = 150
IMG_WIDTH = 150
test_image_generator = ImageDataGenerator(rescale=1./255) 
test_data_gen = test_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=test_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')


sample_test_images, labels = next(test_data_gen)
prediction = model.predict(sample_test_images)

class_names = ['CI', 'HC', 'PO']

# One hot encoded prediction to label encoded
pred=[]
for ix in range(0,batch_size): 
    P = np.argmax(prediction[ix])
    pred.append(P)

#Plotting Confusion Matrix
mat = confusion_matrix(labels, pred)
plot_confusion_matrix(conf_mat=mat, figsize=(4, 4), class_names = class_names, show_normed=False)
plt.show()