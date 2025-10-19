from tensorflow.keras.models import load_model
import cv2 
import numpy as np 
s = load_model("xray.h5")
s.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
l= ["factured","Non factureed"]

c = cv2.imread("BoneFractureDataset/testing/fractured/1-rotated1-rotated1.jpg")



r = cv2.resize(c, (128, 128) )


t = np.array(r) 

t = t.astype('float32') / 255.0 

t_input = np.expand_dims(t, axis=0)


pr = s.predict(t_input)
print(l[np.argmax(pr)])
