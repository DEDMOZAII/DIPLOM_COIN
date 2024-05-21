from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class CoinsKeeper:
    def __init__(self):
        self.n_gen_ = 0
        self.n_fake_l = 0
        self.n_fake_g = 0
        self.k_gen = 0
        self.k_fake_l = 0
        self.k_fake_g = 0
        self.weights = []

    def set_n_gen(self, value):
        self.n_gen_ = value

    def set_n_fake_l(self, value):
        self.n_fake_l = value

    def set_n_fake_g(self, value):
        self.n_fake_g = value

    def set_k_gen(self, value):
        self.k_gen = value

    def set_k_fake_l(self, value):
        self.k_fake_l = value

    def set_k_fake_g(self, value):
        self.k_fake_g = value

    def set_weights(self, weights):
        self.weights = weights

    def load_data_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.n_gen_ = int(lines[0].strip())
            self.n_fake_l = int(lines[1].strip())
            self.n_fake_g = int(lines[2].strip())
            self.k_gen = int(lines[3].strip())
            self.k_fake_l = int(lines[4].strip())
            self.k_fake_g = int(lines[5].strip())
            self.weights = list(map(int, lines[6].strip().split()))

class CoinsDetector:
    def __init__(self, keeper):
        self.keeper = keeper
        self.results = []

    def left_pan(self, k):
        return list(range(0, k))

    def right_pan(self, k):
        return list(range(k, 2 * k))

    def balance(self, vector1, vector2):
        sum_left = sum(self.keeper.weights[i] for i in vector1)
        sum_right = sum(self.keeper.weights[i] for i in vector2)
        return sum_left - sum_right

    def weightingProcess(self):
        left = self.left_pan(self.keeper.k_gen)
        right = self.right_pan(self.keeper.k_gen)
        result = self.balance(left, right)
        return f"Left pan: {left}, Right pan: {right}, Result: {'Left heavier' if result > 0 else 'Right heavier' if result < 0 else 'Balance'}"

def Solver(keeper, detector):
    return detector.weightingProcess()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    data = request.json
    keeper = CoinsKeeper()
    keeper.set_n_gen(data['n_gen'])
    keeper.set_n_fake_l(data['n_fake_l'])
    keeper.set_n_fake_g(data['n_fake_g'])
    keeper.set_k_gen(data['k_gen'])
    keeper.set_k_fake_l(data['k_fake_l'])
    keeper.set_k_fake_g(data['k_fake_g'])
    keeper.set_weights(data['weights'])

    detector = CoinsDetector(keeper)
    result = Solver(keeper, detector)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)