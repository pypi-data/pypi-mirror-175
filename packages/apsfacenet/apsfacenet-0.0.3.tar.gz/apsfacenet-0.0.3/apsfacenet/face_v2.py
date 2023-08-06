from torchvision import transforms
import torch
import torch.nn as nn
from torchvision.models import resnet50

try:
    from torch.hub import load_state_dict_from_url
except ImportError:
    from torch.utils.model_zoo import load_url as load_state_dict_from_url


class Flatten(nn.Module):

    def forward(self, x):
        return x.view(x.size(0), -1)


class FaceNetModel(nn.Module):
    def __init__(self, pretrained=False):
        super(FaceNetModel, self).__init__()

        self.model = resnet50(pretrained)
        embedding_size = 128
        num_classes = 500
        self.cnn = nn.Sequential(
            self.model.conv1,
            self.model.bn1,
            self.model.relu,
            self.model.maxpool,
            self.model.layer1,
            self.model.layer2,
            self.model.layer3,
            self.model.layer4)

        # modify fc layer based on https://arxiv.org/abs/1703.07737
        self.model.fc = nn.Sequential(
            Flatten(),
            # nn.Linear(100352, 1024),
            # nn.BatchNorm1d(1024),
            # nn.ReLU(),
            nn.Linear(100352, embedding_size))

        self.model.classifier = nn.Linear(embedding_size, num_classes)

    def l2_norm(self, input):
        input_size = input.size()
        buffer = torch.pow(input, 2)
        normp = torch.sum(buffer, 1).add_(1e-10)
        norm = torch.sqrt(normp)
        _output = torch.div(input, norm.view(-1, 1).expand_as(input))
        output = _output.view(input_size)
        return output

    def freeze_all(self):
        for param in self.model.parameters():
            param.requires_grad = False

    def unfreeze_all(self):
        for param in self.model.parameters():
            param.requires_grad = True

    def freeze_fc(self):
        for param in self.model.fc.parameters():
            param.requires_grad = False

    def unfreeze_fc(self):
        for param in self.model.fc.parameters():
            param.requires_grad = True

    def freeze_only(self, freeze):
        for name, child in self.model.named_children():
            if name in freeze:
                for param in child.parameters():
                    param.requires_grad = False
            else:
                for param in child.parameters():
                    param.requires_grad = True

    def unfreeze_only(self, unfreeze):
        for name, child in self.model.named_children():
            if name in unfreeze:
                for param in child.parameters():
                    param.requires_grad = True
            else:
                for param in child.parameters():
                    param.requires_grad = False

    # returns face embedding(embedding_size)
    def forward(self, x):
        x = self.cnn(x)
        x = self.model.fc(x)

        features = self.l2_norm(x)
        # Multiply by alpha = 10 as suggested in https://arxiv.org/pdf/1703.09507.pdf
        alpha = 10
        features = features * alpha
        return features

    def forward_classifier(self, x):
        features = self.forward(x)
        res = self.model.classifier(features)
        return res


class FaceVerification:
    '''
    Creates embedding of a image and assist in verifying the identitiy.

    Parameters:
    -----------
    transform : torch transform object
        Contains transformation that are to be applied on an image before the model
    model : torch model
        FaceNet model architecture
    device : torch device
        Specifies the device to be calculated. It's either "gpu" or "cpu"
    model_state_dir : str
        Directory path of the model weights
    lower_threshold : float
        Lower threshold value for verification
    upper_threshold : float
        Upper threshold value for verification
    '''
    def __init__(self, transform=transforms.Compose([
                            transforms.Resize(224),
                            transforms.CenterCrop(224),
                            transforms.ToTensor(),
                        ]),
                        model=FaceNetModel(), device='cuda' if torch.cuda.is_available() else 'cpu',
                        model_state_dir='./testing_section/trained_model/aPS_cattle_face.pth',
                        lower_threshold=2.7, upper_threshold=3.1):
        self.transform = transform
        self.model = model
        self.device = device
        self.model_state_dir = model_state_dir
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def set_model_state_dir(self, model_state_dir):
        self.model_state_dir = model_state_dir

    def set_threshold(self, lower_threshold, upper_threshold):
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

    def get_eval_model(self):
        '''
        Load weight of the facenet model.

        Returns:
        --------
        model : torch model
            FaceNet model with pretrained weight
        '''
        model = self.model
        model.load_state_dict(torch.load(self.model_state_dir, map_location=self.device)['state_dict'])
        model.to(self.device)
        model.eval()
        return model
    
    def get_embedding(self, image_file):
        '''
        Calculates 128 D embedding of an image.

        Parameters:
        -----------
        image_file : PIL image
            Image that need to be embedded
        
        Returns:
        --------
        image_embd : numpy array
            Embedding of the given image
            
        '''
        weighted_model = self.get_eval_model()
        image = self.transform(image_file).reshape(1, 3, 224, 224).to(self.device)
        image_embd = weighted_model(image).detach().cpu().numpy().flatten()
        return image_embd