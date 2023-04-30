from torch import nn


class MyNeuralNet(nn.Module):
    def __init__(self, input_width):
        super().__init__()

        print("input width:", input_width)
        self.layers = nn.Sequential(
            nn.Linear(input_width, 100),
            nn.SELU(),
            nn.Linear(100, 100),
            nn.SELU(),
            nn.Linear(100, 1),
        )

    def forward(self, X, **kwargs):
        y_hat = self.layers(X)
        return y_hat
