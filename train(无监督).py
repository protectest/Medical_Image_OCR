import os
import random
from PIL import Image
import numpy as np
from keras import models
from keras.utils.np_utils import to_categorical


data = list()
label_list = list()
label = [str(i) for i in range(18)]
r = random.random
random.seed(2)
tmp_path = os.path.join('D:/', 'data', 'OCR', 'train_data')
label_name = os.listdir(tmp_path)
diction = {i: j for i, j in list(zip(label, label_name))}
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
label, data = list(zip(*tmp_data))
y_train = to_categorical(label, num_classes=18)
data = np.array(data).reshape((len(data), 20, 20, 1))/255

model = models.load_model('OCR')
loss, accuracy = model.evaluate(data, y_train)
result = model.predict_classes(data)
counter = 0
for i in result:
    counter += 1
    print(diction[str(i)], end='')
    # print(i, end=' ')
print(loss, accuracy)
