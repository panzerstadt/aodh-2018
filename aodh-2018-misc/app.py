import Algorithmia
import json

input = {
  "image_url": "https://i.imgur.com/65Nrqjk.jpg",
  "filter_class": "sky"
}
client = Algorithmia.client('simhFhidXPbHSy2ybtT7c+UB+Nr1')
algo = client.algo('panzerstadt/ImageSegmentationwithPSPNet/0.1.0')

result = json.loads(algo.pipe(input).result)
print(result)
print(type(result))

with open('temp.json', 'w') as f:
    json.dump(result, f)
