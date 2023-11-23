import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from models.resnet import ResNet

# TODO
# 1. 기능별로 코드 분리 (모델 정의 (완), 데이터셋 정의, 학습, 테스트, 저장)
# 2. 모델 Split 코드 추가

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    

train_data, train_labels = torch.load('dataset/mnist/training.pt')
test_data, test_labels = torch.load('dataset/mnist/test.pt')

train_dataset = TensorDataset(train_data.unsqueeze(1).float(), train_labels)
test_dataset = TensorDataset(test_data.unsqueeze(1).float(), test_labels)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)


# Initialize model, loss, and optimizer
model = ResNet().to(device)  # Move model to GPU
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training
for epoch in range(10):
    model.train()
    for i, (data, labels) in enumerate(train_loader):
        data, labels = data.to(device), labels.to(device)  # Move data and labels to GPU
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        if (i + 1) % 100 == 0:
            print(f"Epoch [{epoch + 1}/10], Step [{i + 1}/{len(train_loader)}], Loss: {loss.item():.4f}")

# Testing
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for data, labels in test_loader:
        data, labels = data.to(device), labels.to(device)  # Move data and labels to GPU
        outputs = model(data)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f"Test Accuracy: {100 * correct / total}%")

# Save model
torch.save(model.state_dict(), '../models/mnist-resnet.pt')