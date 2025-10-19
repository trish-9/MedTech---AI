import cv2 as cv
import numpy as np
import tensorflow as tf
from  sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
s = ImageDataGenerator()
train  = s.flow_from_directory("BoneFractureDataset/training",target_size=(128,128),class_mode='binary',batch_size = 32,color_mode = 'rgb')
validat = s.flow_from_directory("BoneFractureDataset/testing",target_size=(128,128),class_mode='binary',batch_size = 32,color_mode = 'rgb')
model = Sequential()
model.add(layers.Conv2D(128,(2,2),input_shape = (128,128,3),activation = "relu"))
model.add(layers.MaxPooling2D(2,2))
model.add(layers.Conv2D(64,(2,2),activation = "relu"))
model.add(layers.MaxPooling2D(2,2))
model.add(layers.Flatten())
model.add(layers.Dense(128,activation = "relu"))
model.add(layers.Dense(64,activation = "relu"))
model.add(layers.Dense(1,activation = "sigmoid"))
model.compile(optimizer = "adam",loss = 'binary_crossentropy',metrics = ['accuracy'])
model.fit(train, epochs = 5  ,steps_per_epoch = 20 , validation_data = validat)
model.save("xray.h5")
