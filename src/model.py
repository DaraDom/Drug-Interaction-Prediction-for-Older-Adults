import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

class Model:
    def __init__(self) -> None:
        self.model = None

    def save_model(self, model_name: str) -> None:
        torch.save(self.model.state_dict(), f"models/{model_name}")

    def load_model(self, model_name: str="default.pth", weights: bool=False) -> None:
        self.model = torch.load(f"models/{model_name}", weights_only=weights)
        

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
    
    def make_prediction(self, inputs: list) -> str:
        inputs = torch.tensor(inputs, dtype=torch.float32)
        self.model.eval()
        with torch.no_grad():
            return self.model(inputs)

class NeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(NeuralNetwork, self).__init__()
        
        # Define multiple layers
        self.layer_1 = nn.Linear(input_dim, hidden_dim // 16)
        nn.init.kaiming_uniform_(self.layer_1.weight, nonlinearity="relu")
        
        self.layer_2 = nn.Linear(hidden_dim // 16, hidden_dim // 32)  # Hidden layer (reduce size)
        nn.init.kaiming_uniform_(self.layer_2.weight, nonlinearity="relu")
        
        self.layer_3 = nn.Linear(hidden_dim // 32, hidden_dim // 64)  # Another hidden layer
        nn.init.kaiming_uniform_(self.layer_3.weight, nonlinearity="relu")

        self.dropout = nn.Dropout(p=0.2)
        
        self.output_layer = nn.Linear(hidden_dim // 64, output_dim)  # Final output layer
        
    def forward(self, x):
        # Pass through layers with ReLU activations
        x = torch.nn.functional.relu(self.layer_1(x))
        x = self.dropout(x)

        x = torch.nn.functional.relu(self.layer_2(x))
        x = self.dropout(x)

        x = torch.nn.functional.relu(self.layer_3(x))
        x = self.dropout(x)

        x = torch.nn.functional.sigmoid(self.output_layer(x))  # Sigmoid for binary output
        return x

class MultiOutputNeuralNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(MultiOutputNeuralNetwork, self).__init__()
        
        # Define multiple layers
        self.layer_1 = nn.Linear(input_dim, hidden_dim // 2 + output_dim)
        nn.init.kaiming_uniform_(self.layer_1.weight, nonlinearity="relu")
        
        self.layer_2 = nn.Linear(hidden_dim // 2 + output_dim, hidden_dim // 4 + output_dim)  # Hidden layer (reduce size)
        nn.init.kaiming_uniform_(self.layer_2.weight, nonlinearity="relu")
        
        self.layer_3 = nn.Linear(hidden_dim // 4 + output_dim, hidden_dim // 8 + output_dim)  # Another hidden layer
        nn.init.kaiming_uniform_(self.layer_3.weight, nonlinearity="relu")

        self.layer_4 = nn.Linear(hidden_dim // 8 + output_dim, hidden_dim // 16 + output_dim)  # Fourth hidden layer
        nn.init.kaiming_uniform_(self.layer_4.weight, nonlinearity="relu")
        
        self.layer_5 = nn.Linear(hidden_dim // 16 + output_dim, hidden_dim // 32 + output_dim)  # Fifth hidden layer
        nn.init.kaiming_uniform_(self.layer_5.weight, nonlinearity="relu")

        self.layer_6 = nn.Linear(hidden_dim // 32 + output_dim, hidden_dim // 64 + output_dim)  # Fourth hidden layer
        nn.init.kaiming_uniform_(self.layer_4.weight, nonlinearity="relu")
        
        self.layer_7 = nn.Linear(hidden_dim // 64 + output_dim, hidden_dim // 128 + output_dim)  # Fifth hidden layer
        nn.init.kaiming_uniform_(self.layer_5.weight, nonlinearity="relu")
        
        self.output_layer = nn.Linear(hidden_dim // 128 + output_dim, output_dim)  # Final output layer

        self.dropout = nn.Dropout(p=0.2)  # Define dropout
        
    def forward(self, x):
        # Pass through layers with ReLU activations
        x = torch.nn.functional.relu(self.layer_1(x))
        x = self.dropout(x)
        x = torch.nn.functional.relu(self.layer_2(x))
        x = self.dropout(x)
        x = torch.nn.functional.relu(self.layer_3(x))
        x = self.dropout(x)
        x = torch.nn.functional.relu(self.layer_4(x))
        x = self.dropout(x)
        x = torch.nn.functional.relu(self.layer_5(x))
        x = self.dropout(x)
        x = torch.nn.functional.relu(self.layer_6(x))
        x = self.dropout(x)
        x = torch.nn.functional.relu(self.layer_7(x))
        x = self.dropout(x)

        x = self.output_layer(x)
        return x

