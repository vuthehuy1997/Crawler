from os import listdir
from os.path import join
import os
import shutil
from PIL import Image
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import pandas as pd

root = 'an_toan_xuat_ban/images'
hs_total = []
ws_total = []
for data in ['train', 'val', 'test']:
    print('_______________{}_________________'.format(data))
    folder_path = join(root, data)
    file_names = (listdir(folder_path))
    file_names.sort()
    # file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x)[0]))
    ws = []
    hs = []

    for file_name in file_names:
        path = join(folder_path, file_name)
        image = Image.open(path)
        w,h = image.size
        ws.append(w)
        hs.append(h)
    hs_total.append(hs)
    ws_total.append(ws)
colors = ["red", "yellow", "green"]
plt.hist(ws, density=True, bins=30, color=colors)  # density=False would make counts
handles = [Rectangle((0, 0), 1, 1, color=c, ec="k") for c in colors]
labels = datasets
plt.legend(handles, labels)
plt.ylabel('Probability')
plt.xlabel('Data')
plt.savefig('width.jpg')
plt.legend()
plt.clf()

colors = ["red", "yellow", "green"]
plt.hist(hs, density=True, bins=30, color=colors)  # density=False would make counts
handles = [Rectangle((0, 0), 1, 1, color=c, ec="k") for c in colors]
labels = datasets
plt.legend(handles, labels)
plt.ylabel('Probability')
plt.xlabel('Data')
plt.savefig('height.jpg')
plt.legend()
plt.clf()

