import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

class Model:
    def __init__(self, input_dim) -> None:
        self.model = self.create_model(input_dim)

    def create_model(self, input_dim) -> nn.Module:
        # DEFAULT
        model = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )
        return model

    def save_model(self, model_name: str) -> None:
        torch.save(self.model.state_dict(), f"models/{model_name}.pt")

    def load_model(self, model_name: str) -> None:
        self.model.load_state_dict(torch.load(f"models/{model_name}.pt", weights_only=True))

    def train_model(self, data, labels, epochs=50, batch_size=32) -> None:
        data = torch.tensor(data, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.float32)

        dataset = TensorDataset(data, labels)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        for epoch in range(epochs):
            epoch_loss = 0
            for inputs, targets in dataloader:
                optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            print(f'Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(dataloader)}')

    def evaluate_model(self, data, labels) -> None:
        data = torch.tensor(data, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.float32)

        self.model.eval()
        with torch.no_grad():
            outputs = self.model(data)
            criterion = nn.MSELoss()
            loss = criterion(outputs, labels)
            print(f'Evaluation Loss: {loss.item()}')