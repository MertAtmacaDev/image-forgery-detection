import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from torchvision.models import resnet18, ResNet18_Weights

def train():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 50)
    print("System Analysis:")
    print(f"Using Device: {device}")
    if torch.cuda.is_available():
        print(f"GPU Model: {torch.cuda.get_device_name(0)}")
    print("=" * 50)

    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../datasets/casia-v2"))
    model_save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "models/cnn_model.pth"))

    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset directory not found!\nLooked at: {dataset_path}")
        print("Please ensure the CASIA v2 dataset is downloaded and placed correctly.")
        return

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    print("Scanning dataset directory...")
    full_dataset = datasets.ImageFolder(root=dataset_path, transform=transform)
    print(f"Total images found: {len(full_dataset)}")
    print(f"Class labels (Folder names): {full_dataset.classes}")
    print(f"Class mapping to indices: {full_dataset.class_to_idx}")

    # %80 training %20 validation split
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    
    generator = torch.Generator().manual_seed(42)
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size], generator=generator)

    batch_size = 32
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print("\nDownloading/Loading Pretrained ResNet18 model...")
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, 2)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 10
    print(f"\nStarting Training Loop ({epochs} Total Epochs)...")
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
    print(f"Training completed successfully! Model saved at:\n-> {model_save_path}")
    print("=" * 50)

if __name__ == "__main__":
    train()