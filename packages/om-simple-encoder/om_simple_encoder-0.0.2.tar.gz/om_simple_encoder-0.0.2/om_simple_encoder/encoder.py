import math
import torch
from om_simple_encoder import CustomCLIPWrapper
from om_simple_encoder.text_image_dm import TextImageDataset
import torch.nn.functional as F
#from sentence_transformers import SentenceTransformer, util
import PIL
from torchvision.models import resnet50
import om_simple_encoder.clip as clip
import timm


class Encoder(object):
    def __init__(self, PATH="best.ckpt"):
        #img_encoder = SentenceTransformer('clip-ViT-B-32')
        img_encoder = resnet50(pretrained=True) 
        img_encoder.fc = torch.nn.Linear(2048, 1000)
        #img_encoder = timm.create_model('swin_base_patch4_window7_224',pretrained=True)
        self.model = CustomCLIPWrapper.load_from_checkpoint(checkpoint_path=PATH, image_encoder=img_encoder, minibatch_size=64)
        self.data_loader = TextImageDataset()
        self.model.eval()



    def images(self, urls):
        images = []
        for url in urls:
            image = self.data_loader.image_transform(PIL.Image.open(url))
            images.append(image)
        image = torch.stack([row for row in images])
        with torch.no_grad():
            ims = F.normalize(self.model.project(self.model.model.encode_image(image)), dim=1)
        return ims


if __name__ == "__main__":
    import glob
    X = Encoder()
    temp = []
    x = X.images(["n02691156_9491-1.png"])
    print (x)
    exit()
