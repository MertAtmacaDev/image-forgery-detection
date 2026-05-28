import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from torchvision.models import resnet18
from PIL import Image

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_CNN_MODEL = None
_CNN_LSTM_MODEL = None

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
CNN_PATH = os.path.join(BASE_DIR, "models/cnn_model.pth")
CNN_LSTM_PATH = os.path.join(BASE_DIR, "models/cnn_lstm_model.pth")

class CnnLstmModel(nn.Module):
    def __init__(self):
        super(CnnLstmModel, self).__init__()
        self.patch_cnn = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.patch_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.lstm = nn.LSTM(input_size=128, hidden_size=64, num_layers=1, batch_first=True)
        self.fc = nn.Linear(64, 2)

    def forward(self, x):
        batch_size, channels, height, width = x.size()
        patch_size = 32
        num_patches_side = 4
        
        patches = x.view(batch_size, channels, num_patches_side, patch_size, num_patches_side, patch_size)
        patches = patches.permute(0, 2, 4, 1, 3, 5).contiguous()
        patches = patches.view(batch_size, 16, channels, patch_size, patch_size)
        
        cnn_input = patches.view(-1, channels, patch_size, patch_size)
        cnn_features = self.patch_cnn(cnn_input)
        cnn_features = self.patch_pool(cnn_features)
        
        lstm_sequence = cnn_features.view(batch_size, 16, 128)
        lstm_out, (hn, cn) = self.lstm(lstm_sequence)
        last_hidden_state = lstm_out[:, -1, :]
        
        logits = self.fc(last_hidden_state)
        return logits

def compute_ela(image_path, quality=90):
    im = cv2.imread(image_path)
    if im is None:
        return None
    success, encoded_img = cv2.imencode('.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not success:
        return im
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    diff = cv2.absdiff(im, decoded_img)
    diff = cv2.multiply(diff, 15)
    return diff

def predict_cnn(image_path: str):
    global _CNN_MODEL
    
    if _CNN_MODEL is None:
        if not os.path.exists(CNN_PATH):
            return {"error": f"Model weights not found at {CNN_PATH}"}
        
        model = resnet18()
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, 2)
        
        model.load_state_dict(torch.load(CNN_PATH, map_location=DEVICE))
        # --- FIXED LINE BELOW (Changed device to DEVICE) ---
        model = model.to(DEVICE)
        model.eval()
        _CNN_MODEL = model

    try:
        pil_img = Image.open(image_path).convert('RGB')
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        input_tensor = transform(pil_img).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            outputs = _CNN_MODEL(input_tensor)
            probabilities = F.softmax(outputs, dim=1).cpu().numpy()[0]
            
        prediction_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[prediction_idx])
        prediction_label = "tampered" if prediction_idx == 1 else "authentic"
        
        return {
            "model": "ResNet18 Transfer Learning",
            "prediction": prediction_label,
            "confidence": confidence
        }
    except Exception as e:
        return {"error": f"CNN Inference failed: {str(e)}"}


def predict_cnn_lstm(image_path: str):
    global _CNN_LSTM_MODEL
    
    if _CNN_LSTM_MODEL is None:
        if not os.path.exists(CNN_LSTM_PATH):
            return {"error": f"Model weights not found at {CNN_LSTM_PATH}"}
            
        model = CnnLstmModel()
        model.load_state_dict(torch.load(CNN_LSTM_PATH, map_location=DEVICE))
        model = model.to(DEVICE)
        model.eval()
        _CNN_LSTM_MODEL = model

    try:
        ela_img = compute_ela(image_path, quality=90)
        if ela_img is None:
            return {"error": "Failed to compute ELA transformation on image."}
            
        ela_img = cv2.cvtColor(ela_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(ela_img)
        
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        input_tensor = transform(pil_img).unsqueeze(0).to(DEVICE)
        
        with torch.no_grad():
            outputs = _CNN_LSTM_MODEL(input_tensor)
            probabilities = F.softmax(outputs, dim=1).cpu().numpy()[0]
            
        prediction_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[prediction_idx])
        prediction_label = "tampered" if prediction_idx == 1 else "authentic"
        
        return {
            "model": "CNN-LSTM Hybrid (ELA)",
            "prediction": prediction_label,
            "confidence": confidence
        }
    except Exception as e:
        return {"error": f"CNN-LSTM Inference failed: {str(e)}"}