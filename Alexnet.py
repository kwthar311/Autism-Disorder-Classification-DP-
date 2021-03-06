# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11pZWIy6MfxKWhoG7bH0nHizNU-Rnckod
"""

import keras
from keras.models import sequential,Model
from keras.layers import Dense,Activation,Dropout,Flatten,Conv2D,Input,MaxPool2D
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

image_shape =(224,224,3)

train_path ='/content/drive/MyDrive/Colab Notebooks/train/train'
test_path = '/content/drive/MyDrive/Colab Notebooks/test/test'

from keras.preprocessing.image import ImageDataGenerator

# create a new generator
imagegen = ImageDataGenerator()
# load train data
train = imagegen.flow_from_directory(train_path, class_mode="categorical", shuffle=False, batch_size=100, target_size=(224, 224))
# load val data
val = imagegen.flow_from_directory(test_path, class_mode="categorical", shuffle=False, batch_size=100, target_size=(224, 224))
# load val data

def alexnet(input_shape,n_classes):
  input = Input(input_shape)
  
  # actually batch normalization didn't exist back then
  # they used LRN (Local Response Normalization) for regularization
  x = Conv2D(96, 11, strides=4, padding='same', activation='relu')(input)
  x = BatchNormalization()(x)
  x = MaxPool2D(3, strides=2)(x)
  
  x = Conv2D(256, 5, padding='same', activation='relu')(x)
  x = BatchNormalization()(x)
  x = MaxPool2D(3, strides=2)(x)
  
  x = Conv2D(384, 3, strides=1, padding='same', activation='relu')(x)
  
  x = Conv2D(384, 3, strides=1, padding='same', activation='relu')(x)
  
  x = Conv2D(256, 3, strides=1, padding='same', activation='relu')(x)
  x = BatchNormalization()(x)
  x = MaxPool2D(3, strides=2)(x)
  
  x = Flatten()(x)
  x = Dense(4096, activation='relu')(x)
  x = Dense(4096, activation='relu')(x)
  
  output = Dense(n_classes, activation='softmax')(x)
  
  model = Model(input, output)
  return model

num =2
model =alexnet(image_shape,num)
model.summary()
opt =keras.optimizers.Adam(learning_rate=0.00001)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
# fit on data for 30 epochs
model.fit_generator(train, epochs=40, validation_data=val)
model.save("alexnet.h5")

import os
from keras.preprocessing import image
import matplotlib.pyplot as plt
from keras.models import load_model
import pandas as pd

my_img =[]
labels =[]
path =test_path
for i in os.listdir(path):
  my_img.append(i)
  img=image.load_img(path +'//'+i)
  x =image.array_to_img(img)
  x =np.expand_dims(img,axis=0)
  sav= load_model("alexnet.h5")
  out =sav.predict(x)
  print(out)
  if out[0][1]> out[0][0]:
    print("non_autistic")
    label = 0
    labels.append(label)
  else:
    print("autistic")
    label = 1
    labels.append(label)
submit =pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Submit.csv')
submit['Image'] = my_img
print(submit['Image'])
submit['Label'] = labels
submit.to_csv("submit1.csv",index=False)
#print("Done!")