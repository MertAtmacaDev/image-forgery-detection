import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image

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

class CasiaElaDataset(Dataset):
    def __init__(self, root_dir, transform=None, quality=90):
        self.root_dir = root_dir
        self.transform = transform
        self.quality = quality
        self.image_paths = []
        self.labels = []
        self.class_to_idx = {"Au": 0, "Tp": 1}
        
        for class_name in ["Au", "Tp"]:
            class_dir = os.path.join(root_dir, class_name)
            if not os.path.exists(class_dir):
                continue
            for filename in os.listdir(class_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
                    self.image_paths.append(os.path.join(class_dir, filename))
                    self.labels.append(self.class_to_idx[class_name])

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        
        ela_img = compute_ela(img_path, self.quality)
        if ela_img is None:
            ela_img = np.zeros((128, 128, 3), dtype=np.uint8)
            
        ela_img = cv2.cvtColor(ela_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(ela_img)
        
        if self.transform:
            pil_img = self.transform(pil_img)
            
        return pil_img, label

class CnnLstmModel(nn.Module):
    def __init__(self):
        super(CnnLstmModel, self).__init__()
        
        self.patch_cnn = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2), # 32x32 -> 16x16
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2), # 16x16 -> 8x8
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2) # 8x8 -> 4x4
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

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 50)
    print("System Analysis:")
    print(f"Using Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU Model: {torch.cuda.get_device_name(0)}")
    print("=" * 50)

    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../datasets/casia-v2"))
    model_save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "models/cnn_lstm_model.pth"))

    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset directory not found!\nLooked at: {dataset_path}")
        return

    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    print("Initializing Custom ELA Dataset...")
    full_dataset = CasiaElaDataset(root_dir=dataset_path, transform=transform, quality=90)
    print(f"Total images found: {len(full_dataset)}")

    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    generator = torch.Generator().manual_seed(42)
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size], generator=generator)

    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    model = CnnLstmModel().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 10
    print(f"\nStarting CNN-LSTM Hybrid Training Loop ({epochs} Total Epochs)...")
    print("-" * 50)

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total_train += labels.size(0)
            correct_train += (predicted == labels).sum().item()
            
        epoch_loss = running_loss / len(train_dataset)
        train_acc = 100 * correct_train / total_train
        
        model.eval()
        correct_val = 0
        total_val = 0
        val_loss = 0.0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                
                _, predicted = torch.max(outputs.data, 1)
                total_val += labels.size(0)
                correct_val += (predicted == labels).sum().item()
                
        epoch_val_loss = val_loss / len(val_dataset)
        val_acc = 100 * correct_val / total_val
        
        print(f"Epoch [{epoch+1:02d}/{epochs}] -> "
              f"Train Loss: {epoch_loss:.4f} | Train Acc: {train_acc:.2f}% | "
              f"Val Loss: {epoch_val_loss:.4f} | Val Acc: {val_acc:.2f}%")

    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    torch.save(model.state_dict(), model_save_path)
    print("-" * 50)
    print(f"Hybrid model saved successfully at:\n-> {model_save_path}")
    print("=" * 50)

if __name__ == "__main__":
    train()