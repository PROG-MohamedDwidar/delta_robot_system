import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.callbacks import EarlyStopping
import pandas as pd


#normalization function that uses the min as (-500) and max as (500) to normalize the dataframe
def normalizeI(df):
    return (df + 500) / 1000
def denormalizeI(df):
    return (df * 1000) - 500
#normalization function that uses the min as (-90) and max as (90) to normalize the angles in dataframe
def normalizeA(df):
    return (df + 90) / 180
def denormalizeA(df):
    return (df * 180) - 90




#read dataframe 
df = pd.read_csv('data.csv')
#normalize the dataframe
df['x'] = normalizeI(df['x'])
df['y'] = normalizeI(df['y'])
df['z'] = normalizeI(df['z'])
df['t1'] = normalizeA(df['t1'])
df['t2'] = normalizeA(df['t2'])
df['t3'] = normalizeA(df['t3'])
#split the dataframe into 80% training and 10% validation and 10% test
train = df.sample(frac=0.8,random_state=2324)
#remove the training data from the dataframe
df = df.drop(train.index)
val = df.sample(frac=0.5,random_state=20234)
df = df.drop(val.index)
test = df

#split the data into input and output
train_x = train[['x','y','z']]
train_y = train[['t1','t2','t3']]
val_x = val[['x','y','z']]
val_y = val[['t1','t2','t3']]
test_x = test[['x','y','z']]
test_y = test[['t1','t2','t3']]

callback = EarlyStopping(monitor='val_loss', patience=3)
#build the model
model = Sequential()




model.add(Dense(64,activation='relu',input_shape=(3,)))
model.add(Dense(64,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(3))
model.compile(optimizer=Adam(),loss=MeanSquaredError())
#model.load_weights('model.h5')
model.fit(train_x,train_y,epochs=15,validation_data=(val_x,val_y),batch_size=2,callbacks=[callback])

#test the model
model.evaluate(test_x,test_y)
#save the model weights
model.save_weights('modelNorm.h5')

#print the model summary
#print(model.summary())
#draw the loss graph
import matplotlib.pyplot as plt
print(model.history.history.keys())
#plt.show()

#print 
