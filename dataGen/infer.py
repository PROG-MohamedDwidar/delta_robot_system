import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import pandas as pd


model = Sequential()
model.add(Dense(64,activation='relu',input_shape=(3,)))
model.add(Dense(64,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(3))
model.compile(optimizer=Adam(),loss=MeanSquaredError())
model.load_weights('model.h5')

while True:
    x = float(input("Enter x: "))
    y = float(input("Enter y: "))
    z = float(input("Enter z: "))
    print(model.predict([[x,y,z]]))