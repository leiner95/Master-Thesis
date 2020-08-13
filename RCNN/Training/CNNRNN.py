import os
import glob
import tensorflow as tf
import tensorflow.keras as keras
from keras_video import VideoFrameGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, BatchNormalization, MaxPooling2D, GlobalMaxPool2D, Flatten
from tensorflow.keras.layers import TimeDistributed, GRU, Dense, Dropout, LSTM
with tf.device('/gpu:0'):
    # use sub directories names as classes
    classes = [i.split(os.path.sep)[1] for i in glob.glob('videos/*')]
    classes.sort()
    # some global params
    SIZE = (150, 150)
    CHANNELS = 3
    NBFRAME = 5
    BS = 10
    # pattern to get videos and classes
    glob_pattern='videos/{classname}/*.avi'
    # for data augmentation
    data_aug = keras.preprocessing.image.ImageDataGenerator(
        zoom_range=.1,
        horizontal_flip=True,
        rotation_range=8,
        width_shift_range=.2,
        height_shift_range=.2)
    # Create video frame generator
    # change parameter split for validation data
    train = VideoFrameGenerator(
        classes=classes, 
        glob_pattern=glob_pattern,
        nb_frames=NBFRAME,
        split=.2, 
        shuffle=True,
        batch_size=BS,
        target_shape=SIZE,
        nb_channel=CHANNELS,
        transformation=data_aug,
        use_frame_cache=True)
    # Validation data
    valid = train.get_validation_generator()

    # Here the AlexNet starts
    cnn= Sequential()
    cnn.add(Conv2D(96, 11 ,strides=4, input_shape=(150, 150, 3), padding='same', activation='relu'))
    cnn.add(MaxPooling2D(3, strides=2)),
    cnn.add(Conv2D(56, 5, strides=1, activation='relu', padding='same')),
    cnn.add(MaxPooling2D(3, strides=2)),
    cnn.add(Conv2D(384, 3, strides=1, activation='relu', padding='same')),
    cnn.add(Conv2D(384, 3, strides=1, activation='relu', padding='same')),
    cnn.add(Conv2D(256, 3, strides=1, activation='relu', padding='same')),
    cnn.add(GlobalMaxPool2D())
    # Now the recurrent part starts
    model= Sequential()
    model.add(TimeDistributed(cnn, input_shape=(5, 150, 150, 3)))
    model.add(LSTM(64))
    # At the end the feed forward, fully connected part
    Dense(4096, activation='relu'),
    Dropout(0.5),
    Dense(4096, activation='relu'),
    Dropout(0.5),
    model.add(Dense(2, activation='softmax'))
    
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])
    model.summary()

    EPOCHS=2
    
    model.fit_generator(
        train,
        validation_data=valid,
        validation_steps=753,
        validation_freq=1,
        verbose=1,
        epochs=EPOCHS,
        steps_per_epoch= 3014
    )

    model.save('RCNNmodel.h5')
 