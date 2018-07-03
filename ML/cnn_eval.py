# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 10:24:25 2018

@author: Kevin Mulder
"""

from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from PIL import Image
import glob
import numpy as np
import PIL
from PIL import Image
num_classes = 2

img_rows, img_cols = 64, 64
input_shape = (img_rows, img_cols, 3)

for i in range(1,11):
    image_list=glob.glob('plant%i.jpg'%i)
    img = load_img(image_list[0])  # this is a PIL image
    x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)
    
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    
    opt = keras.optimizers.SGD(lr=0.01)
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=opt,
                  metrics=['accuracy'])
    model.load_weights('leaf-model_resized.h5')
    
    print(model.predict_classes(x,batch_size=1))
