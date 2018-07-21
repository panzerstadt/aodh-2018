import Algorithmia

input = {
  "image_url": "https://i.imgur.com/zxTNS3e.jpg",
  "filter_class": "sky"
}
client = Algorithmia.client('simhFhidXPbHSy2ybtT7c+UB+Nr1')
algo = client.algo('panzerstadt/ImageSegmentationwithPSPNet/0.1.0')
print(algo.pipe(input).result)