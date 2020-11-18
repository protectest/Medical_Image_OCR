import os
import random
from PIL import Image
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Convolution2D, MaxPooling2D, Flatten
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical


data = list()
label_list = list()
label = [str(i) for i in range(18)]
r = random.random
random.seed(2)
tmp_path = os.path.join('D:/', 'data', 'OCR', 'train_data')
label_name = os.listdir(tmp_path)
diction = {i: j for i, j in list(zip(label_name, label))}
for i in range(len(label_name)):
    path = os.path.join(tmp_path, label_name[i])
    tmp0 = os.listdir(path)
    tmp1 = len(tmp0)*(label[i] + '.')
    tmp1 = tmp1.split('.')
    label_list.extend(tmp1[:-1])
    for j in tmp0:
        photo_path = os.path.join(path, j)
        data.append(np.array(Image.open(photo_path), dtype=int))
tmp_data = list(zip(label_list, data))
random.shuffle(tmp_data)
label, data = list(zip(*tmp_data))
y_train = to_categorical(label, num_classes=18)
data = np.array(data).reshape((len(data), 20, 20, 1))/255

model = Sequential()
model.add(Convolution2D(activation='tanh', input_shape=(20, 20, 1), padding='same', kernel_size=5, filters=32, strides=1))
model.add(MaxPooling2D(pool_size=2, strides=2, padding='same'))
model.add(Convolution2D(filters=64, kernel_size=5, strides=1, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2, strides=2, padding='same'))
model.add(Flatten())
model.add(Dense(units=1024, activation='tanh'))
model.add(Dropout(0.5))
model.add(Dense(units=18, activation='softmax'))
adam = Adam(lr=1e-4)
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(data, y_train, batch_size=64, epochs=50)
loss, accuracy = model.evaluate(data, y_train)
print(loss, accuracy)
model.save('OCR')
