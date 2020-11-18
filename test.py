from PIL import Image
from PIL import ImageFilter
import PIL.ImageOps
import numpy as np
import os
import keras


def function(x):
    if x == '.':
        return '·'
    else:
        return x


label = [str(i) for i in range(18)]
tmp_path = os.path.join('D:/', 'data', 'OCR', 'train_data')
label_name = os.listdir(tmp_path)
diction = {i: j for i, j in list(zip(label, label_name))}

output = list()
fail_list = list()
counter = 0
label = os.listdir(r'D:\data\image')
label0 = ['RA9===.jpg']
model = keras.models.load_model('OCR')
result = list()

for name in label:
    result = list()
    tmp0 = os.path.join('D:/', 'data', 'image', name)
    image = Image.open(tmp0)
    image = image.convert('L')
    image = image.filter(ImageFilter.FIND_EDGES)
    image = PIL.ImageOps.invert(image)
    threshold = 90
    table = [int(i > threshold) for i in range(256)]
    photo = image.point(table, '1')
    photo = photo.filter(ImageFilter.SMOOTH_MORE)
    data = np.array(photo, dtype=int)
    for i in range(photo.size[0]):
        for j in range(photo.size[1]):
            if data[j, i] == 0:
                if data[min(j + 1, photo.size[1] - 2), i] == 1 and data[j - 1, i] == 1:
                    if data[min(j + 1, photo.size[1] - 2), i - 1] == 1 and data[j - 1, i - 1] == 1:
                        if data[min(j + 1, photo.size[1] - 2), min(i + 1, photo.size[0] - 2)] == 1 and data[j - 1, min(i + 1, photo.size[0] - 2)] == 1:
                            data[j, i] = 1
                if data[j, i - 1] == 1 and data[j, min(i + 1, photo.size[0] - 2)] == 1:
                    if data[j - 1, i - 1] == 1 and data[j - 1, min(i + 1, photo.size[0] - 2)] == 1:
                        if data[min(j + 1, photo.size[1] - 1), i - 2] == 1 and data[min(j + 1, photo.size[1] - 2), min(i + 1, photo.size[0] - 2)] == 1:
                            data[j, i] = 1
    photo = PIL.Image.fromarray(data*255)
    height = 0
    width = 0
    tmp1 = data.sum(axis=0)
    for i in range(len(tmp1)):
        if min(tmp1) in tmp1[i: i + 50]:
            if len(tmp1) - i < 220:
                height = (len(tmp1) - 220, len(tmp1))
            else:
                height = (i, i + 220)
            break
    tmp1 = data.sum(axis=1)
    for i in range(len(tmp1)):
        if min(tmp1) in tmp1[i: i + 25]:
            if len(tmp1) - i < 25:
                width = (len(tmp1) - 50, len(tmp1))
            else:
                width = (i, i + 50)
            break

    region = photo.crop((height[0], width[0], height[1], width[1]))
    region = region.convert('L')
    region = region.point(table, '1')
    tmp = np.array(region, dtype=int)
    axis0 = tmp.sum(axis=0)
    axis1 = tmp.sum(axis=1)
    split0L = list()
    split0R = list()
    split1L = 0
    split1R = 0

    for j in range(1, len(axis1)):
        if (axis1[j - 1] < 219) and (axis1[j] >= 219):
            split1R = j
    for j in range(len(axis1) - 1):
        if (axis1[j + 1] < 219) and (axis1[j] >= 219):
            split1L = j

    for j in range(1, len(axis0)):
        if (axis0[j - 1] < 49) and axis0[j] == 49:
            for k in range(len(tmp[:, j])):
                if tmp[:, j][k] == 0:
                    if k >= (split1L + split1R)/2:
                        if axis0[j + 1] == 48 and axis0[j + 2] == 48 and axis0[j + 3] == 48:
                            break
                        else:
                            split0R.append(j)
        if ((axis0[j - 1] < 49) and (axis0[j] > 49)) or (axis0[j - 1] == 48 and axis0[j - 2] == 48 and axis0[j - 3] == 48 and axis0[j - 4] == 48and axis0[j] < 48):
            split0R.append(j)
    for j in range(len(axis0) - 1):
        if (axis0[j + 1] < 49) and axis0[j] == 49:
            for k in range(len(tmp[:, j])):
                if tmp[:, j][k] == 0:
                    if k >= (split1L + split1R)/2:
                        if axis0[j + 1] == 48 and axis0[j + 2] == 48 and axis0[j + 3] == 48:
                            break
                        else:
                            split0L.append(j)
        if ((axis0[j + 1] < 49) and (axis0[j] > 49)) or (j == 0 and axis0[j] < 49) or (axis0[j - 1] == 48 and axis0[j - 2] == 48 and axis0[j - 3] == 48 and axis0[j] == 48 and axis0[j + 1] < 48):
            split0L.append(j)

    image_list = list()

    try:
        for j in range(len(split0R)):
            region_region = region.crop((split0L[j], split1L, split0R[j], split1R))
            new = Image.new('L', (20, 20), 225)
            new.paste(region_region, (0, 0))
            new = new.point(table, '1')
            image_list.append(new)
    except:
        fail_list.append(name)
        continue
    for j in range(len(image_list)):
        tmp_result = model.predict(np.array(image_list[j], dtype=int).reshape((1, 20, 20, 1)))
        if np.max(tmp_result) > 0.95:
            result.append(tmp_result)
        else:
            break
    else:
        tmp_tmp = str()
        for i in result:
            tmp_tmp += diction[str(int((np.where(i == np.max(i)))[1]))]
        output.append(tmp_tmp)
        counter += 1
        continue
    result = list()
    split0L = list()
    split0R = list()
    for j in range(1, len(axis1)):
        if (axis1[j - 1] < 219) and (axis1[j] >= 219):
            split1R = j
    for j in range(len(axis1) - 1):
        if (axis1[j + 1] < 219) and (axis1[j] >= 219):
            split1L = j
    for j in range(1, len(axis0)):
        if (axis0[j - 1] < 49) and axis0[j] == 49:
            for k in range(len(tmp[:, j])):
                if tmp[:, j][k] == 0:
                    if k >= (split1L + split1R) / 2:
                        if axis0[j + 1] == 48 and axis0[j + 2] == 48 and axis0[j + 3] == 48:
                            break
                        else:
                            split0R.append(j)
        if ((axis0[j - 1] < 48) and (axis0[j] >= 48)) or (
                axis0[j - 1] == 48 and axis0[j - 2] == 48 and axis0[j - 3] == 48 and axis0[j - 4] == 48 and
                axis0[j] < 48):
            split0R.append(j)
    for j in range(len(axis0) - 1):
        if (axis0[j + 1] < 49) and axis0[j] == 49:
            for k in range(len(tmp[:, j])):
                if tmp[:, j][k] == 0:
                    if k >= (split1L + split1R) / 2:
                        if axis0[j + 1] == 48 and axis0[j + 2] == 48 and axis0[j + 3] == 48:
                            break
                        else:
                            split0L.append(j)
        if ((axis0[j + 1] < 48) and (axis0[j] >= 48)) or (j == 0 and axis0[j] < 49) or (
                axis0[j - 1] == 48 and axis0[j - 2] == 48 and axis0[j - 3] == 48 and axis0[j] == 48 and
                axis0[j + 1] < 48):
            split0L.append(j)
    image_list = list()
    try:
        for j in range(len(split0R)):
            region_region = region.crop((split0L[j], split1L, split0R[j], split1R))
            new = Image.new('L', (20, 20), 225)
            new.paste(region_region, (0, 0))
            new = new.point(table, '1')
            image_list.append(new)
    except:
        fail_list.append(name)
        continue
    for j in range(len(image_list)):
        tmp_result = model.predict(np.array(image_list[j]).reshape((1, 20, 20, 1)))
        if np.max(tmp_result) > 0.95:
            result.append(tmp_result)
        else:
            fail_list.append(name)
            break
    else:
        counter += 1
        tmp_tmp = str()
        for i in result:
            tmp_tmp += diction[str(int((np.where(i == np.max(i)))[1]))]
        output.append(tmp_tmp)
    print('\r{}%'.format(int(counter*100/len(label))), end='')

print(len(output))
for i in output:
    print(i)

print()
print('*'*20)
print('Fail_list')
for i in fail_list:
    print(i)
print(counter)
print(counter/len(label))





