# Om Simple Encoder
Om Simple Encoder is to fintune the query encoder. Currently it includes only query image encoder. 

# How to start training
```
python train.py --img_dir {image_root_path} --data {data json} --num_workers=15 --gpus=1 --batch_size=64 
```

# Data Format
```json
[ {"key1": ["/path/image1.jpg","/path/image2.jpg"], "key2":  ["/path/image1.jpg","/path/image2.jpg"]},...]
```
