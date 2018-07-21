import json, shutil
from utils.img_utils import show_base64_image, save_base64_image
import requests

import os
print(os.path.isfile('temp.json'))
print(os.getcwd())

with open('temp.json', 'r') as f:
    test_file = json.load(f)

print(test_file)

for k, v in test_file.items():
    print(k)

show_base64_image(test_file['filtered_image'])
save_base64_image(test_file['filtered_image'], 'temp.png')

img_url = "https://i.imgur.com/65Nrqjk.jpg"
response = requests.get(img_url, stream=True)
with open('original.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response