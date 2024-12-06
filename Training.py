import torch
import torch.nn as nn
import torch.optim as optim
import json

trainingData = []
with open('training_data.json', 'r') as json_file:
    trainingData = json.load(json_file)

inputs = []
expectedOutputs = []
for entry in trainingData:
    input = entry["inputs"]["rays"]
    input.append(entry["inputs"]["speed"])
    inputs.append(input)

    expectedOutputs.append(entry["outputs"]["drive"])

inputs = torch.tensor(inputs, dtype=torch.float32)
expectedOutputs = torch.tensor(expectedOutputs, dtype=torch.float32)

model = nn.Sequential(
    nn.Linear(7, 32),
    nn.ReLU(),
    nn.Linear(32, 16),
    nn.ReLU(),
    nn.Linear(16, 2)
)

criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

running_loss = 0
epochs = 10000
for epoch in range(epochs):
    model.train()

    predictions = model(inputs)
    loss = criterion(predictions, expectedOutputs)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    running_loss = loss.item()

    print(f"Epoch {epoch + 1}, Loss: {running_loss:.4f}")

torch.save(model, "GPT5.pth")

print(f"Done Training with {(100 - (running_loss * 100)):.4f} Accuracy")