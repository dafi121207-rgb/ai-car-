import numpy as np
import json

class NeuralNetwork:
    def __init__(self, input_size=7, hidden1=12, hidden2=12, output_size=1):
        self.w1 = np.random.uniform(-1.0, 1.0, (input_size, hidden1))
        self.b1 = np.random.uniform(-1.0, 1.0, (1, hidden1))

        self.w2 = np.random.uniform(-1.0, 1.0, (hidden1, hidden2))
        self.b2 = np.random.uniform(-1.0, 1.0, (1, hidden2))

        self.w3 = np.random.uniform(-1.0, 1.0, (hidden2, output_size))
        self.b3 = np.random.uniform(-1.0, 1.0, (1, output_size))

    def forward(self, inputs):
        X = np.array(inputs).reshape(1, -1)
        h1_raw = np.dot(X, self.w1) + self.b1
        h1_out = np.tanh(h1_raw)
        
        # Layer 2
        h2_raw = np.dot(h1_out, self.w2) + self.b2
        h2_out = np.tanh(h2_raw)
        
        # Output Layer
        out_raw = np.dot(h2_out, self.w3) + self.b3
        output = np.tanh(out_raw)

        self.last_inputs = inputs
        self.last_h1 = h1_out[0]
        self.last_h2 = h2_out[0]
        self.last_hidden = h2_out[0]
        self.last_output = [output[0][0]]

        return output[0][0]

    def save_to_file(self, filename="best_brain.json", generation=1):
        data = {
            "generation": generation,
            "w1": self.w1.tolist(),
            "b1": self.b1.tolist(),
            "w2": self.w2.tolist(),
            "b2": self.b2.tolist(),
            "w3": self.w3.tolist(),
            "b3": self.b3.tolist()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[SUCCESS] Otak AI disimpan ke '{filename}'")

    def load_from_file(self, filename="best_brain.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.w1 = np.array(data["w1"]); 
            self.b1 = np.array(data["b1"])
            self.w2 = np.array(data["w2"]); 
            self.b2 = np.array(data["b2"])
            self.w3 = np.array(data["w3"]); 
            self.b3 = np.array(data["b3"])
            print(f"[SUCCESS] Otak AI dimuat dari '{filename}'")
            return data.get("generation", 1)
        except FileNotFoundError:
            print(f"[ERROR] File '{filename}' tidak ditemukan.")
            return None