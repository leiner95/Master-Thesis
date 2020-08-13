from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import TensorBoard
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

with tf.device('/gpu:0'):
    # PFADE ZU TRAININGS; VALIDATION UND TESTBILDERN
    train_dir = 'F:/DataCNN/5/train'
    validation_dir = 'F:/DataCNN/5/val'





    train_class1_dir = os.path.join(train_dir, 'PO')  # directory with our training class1 pictures
    train_class2_dir = os.path.join(train_dir, 'CI')  # directory with our training class2 pictures
    train_class3_dir = os.path.join(train_dir, 'HC')  # directory with our training class2 pictures
    validation_class1_dir = os.path.join(validation_dir, 'PO')  # directory with our validation class1 pictures
    validation_class2_dir = os.path.join(validation_dir, 'CI')  # directory with our validation class2 pictures
    validation_class3_dir = os.path.join(validation_dir, 'HC')  # directory with our validation class2 pictures
    # Check the data
    num_class1_tr = len(os.listdir(train_class1_dir))
    num_class2_tr = len(os.listdir(train_class2_dir))
    num_class3_tr = len(os.listdir(train_class3_dir))
    num_class1_val = len(os.listdir(validation_class1_dir))
    num_class2_val = len(os.listdir(validation_class2_dir))
    num_class3_val = len(os.listdir(validation_class3_dir))
    total_train = num_class1_tr + num_class2_tr + num_class3_tr
    total_val = num_class1_val + num_class2_val + num_class3_val



    # Loading Images
    batch_size = 150 #Increase for higher amount of data
    epochs = 5 #Increase for higher amount and more complex of data
    IMG_HEIGHT = 150
    IMG_WIDTH = 150

    train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
    validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data



    # tensorflow.keras.preprocessing.image().flow_from_directory() Takes the path to a directory & generates batches of augmented data
    train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                            directory=train_dir,
                                                            shuffle=True,
                                                            target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                            class_mode='binary')

    val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                                directory=validation_dir,
                                                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                                class_mode='binary')


    # NEURONAL NETWORK is generated
    model = Sequential([
        Conv2D(96, 11, strides=4, activation='relu', padding='same', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
        MaxPooling2D(3, strides=2),
        Conv2D(56, 5, strides=1, activation='relu', padding='same'),
        MaxPooling2D(3, strides=2),
        Conv2D(384, 3, strides=1, activation='relu', padding='same'),
        Conv2D(384, 3, strides=1, activation='relu', padding='same'),
        Conv2D(256, 3, strides=1, activation='relu', padding='same'),
        MaxPooling2D(3, strides=2),
        Flatten(),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(4096, activation='relu'),
        Dropout(0.5),
        Dense(3, activation='softmax')
    ])

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    model.summary()

    #Training the Model
    history = model.fit_generator(
        train_data_gen,
        steps_per_epoch= total_train/batch_size,
        epochs=epochs,
        validation_data=val_data_gen,
        validation_steps=total_val/batch_size
        #callbacks=[tensorboard]
    )

    #change names as desired
    model.save("Alexnet_model.h5")

 