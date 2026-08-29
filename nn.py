import numpy as np
import json

class NeuralNetwork:
    def __init__(self, input_size=7, hidden_size=6, output_size=1):
        self.w1 = np.random.uniform(-1.0, 1.0, (input_size, hidden_size))
        self.b1 = np.random.uniform(-1.0, 1.0, (1, hidden_size))
        self.w2 = np.random.uniform(-1.0, 1.0, (hidden_size, output_size))
        self.b2 = np.random.uniform(-1.0, 1.0, (1, output_size))

    def forward(self, inputs):
        X = np.array(inputs).reshape(1, -1)
        hidden_raw = np.dot(X, self.w1) + self.b1
        hidden_out = np.tanh(hidden_raw)
        output_raw = np.dot(hidden_out, self.w2) + self.b2
        output = np.tanh(output_raw)
        return output[0][0]

    def save_to_file(self, filename="best_brain.json"):
        data = {
            "w1": self.w1.tolist(),
            "b1": self.b1.tolist(),
            "w2": self.w2.tolist(),
            "b2": self.b2.tolist()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[SUCCESS] Otak AI disimpan ke '{filename}'")

    def load_from_file(self, filename="best_brain.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.w1 = np.array(data["w1"])
            self.b1 = np.array(data["b1"])
            self.w2 = np.array(data["w2"])
            self.b2 = np.array(data["b2"])
            print(f"[SUCCESS] Otak AI dimuat dari '{filename}'")
            return True
        except FileNotFoundError:
            print(f"[ERROR] File '{filename}' tidak ditemukan.")
            return False