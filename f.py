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
import pandas as pd
s = cv.imread("Acne-2/Train/Acne/acne-039-v2__ProtectWyJQcm90ZWN0Il0_FocusFillWzI5NCwyMjIsIngiLDFd_JPG_jpg.rf.d73d945d15f106bb2eaff2fa26a8e9cb.jpg")
print(np.array(s).shape)
p = ImageDataGenerator()
validate1 = p.flow_from_directory("Acne-2/Train",target_size=(128, 128),class_mode='categorical',shuffle=True,interpolation='nearest',keep_aspect_ratio=False)
validat = p.flow_from_directory("Acne-2/Validation",target_size=(128, 128),class_mode='categorical',shuffle=True,interpolation='nearest',keep_aspect_ratio=False)
#print(validate.class_indices)
#print(validate.class_indices)
model = Sequential()
model.add(layers.Conv2D(64,(2,2),activation = "relu", input_shape = (128,128,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(32,(2,2),activation = "relu"))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(128,activation = "relu"))
model.add(layers.Dense(64,activation = "relu"))
model.add(layers.Dense(3 , activation = "softmax"))
model.compile(optimizer = "adam",loss = 'categorical_crossentropy',metrics = ['accuracy'])
model.fit(validate1, epochs = 5 ,steps_per_epoch = 10 ,validation_data = validat)
model.save("sk.h5")

