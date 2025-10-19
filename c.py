import cv2
import numpy as np
from tensorflow.keras.models import load_model

s = load_model("sk.h5")
s.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
l = ["Acne","Comedo","Clear"]


c = cv2.imread("1.png")



r = cv2.resize(c, (128, 128) )


t = np.array(r) 

t = t.astype('float32') / 255.0 

t_input = np.expand_dims(t, axis=0)


pr = s.predict(t_input)
print(l[np.argmax(pr)])

