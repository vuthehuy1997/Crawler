from os import listdir
from os.path import join
import os
import shutil
import pandas as pd

root = './ndl_v2/labels'
for data in ['train', 'val', 'test']:
    print('_______________{}_________________'.format(data))
    path = join(root, data)
    file_names = (listdir(path))
    file_names.sort()
    # file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x)[0]))

    result = []
    count_image = 0
    count_image_nor = 0
    count_box = 0
    total = 0
    for file_name in file_names:
        if file_name == 'classes.txt':
            continue
        # print(file_name)
        name = os.path.splitext(file_name)[0]
        total += 1
        file_label = 'normal' # 
        lines = open(os.path.join(path,file_name), "r")
        image = 0
        for line in lines:
            line = line.split()
            # print('line: ', line)
            points = list(map(float, line[1:5]))
            label = int(line[0])
            if label == 0:
                image = 1
                count_box += 1
        count_image += image
        if image == 0:
            count_image_nor += 1

    print(total, count_image, count_image_nor, count_box)
# df = pd.DataFrame(result,
#                columns =['file_name', 'label'])
# df.to_csv('./labels/val.csv', index=False)

