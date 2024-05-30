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

    def validate(self):
        total_known = self.n_gen_ + self.n_fake_l + self.n_fake_g
        total_unknown = self.k_gen + self.k_fake_l + self.k_fake_g
        total_coins = total_known + total_unknown
        if total_coins != len(self.weights):
            raise ValueError("The number of coins does not match the number of weights provided.")

class CoinsDetector:
    def __init__(self, keeper):
        self.keeper = keeper
        self.results = []

    def weigh(self, group1, group2):
        sum1 = sum(self.keeper.weights[i] for i in group1)
        sum2 = sum(self.keeper.weights[i] for i in group2)
        self.results.append((group1, group2, sum1, sum2))
        if sum1 == sum2:
            return 0
        return -1 if sum1 < sum2 else 1

    def find_fake_coin(self):
        indices = list(range(len(self.keeper.weights)))
        return self._find_fake_coin_recursive(indices)

    def _find_fake_coin_recursive(self, indices):
        if len(indices) == 1:
            return indices[0]

        third = len(indices) // 3
        group1 = indices[:third]
        group2 = indices[third:2*third]
        group3 = indices[2*third:]

        if len(group1) == 0 or len(group2) == 0:
            group1 = indices[:len(indices)//2]
            group2 = indices[len(indices)//2:]

        result = self.weigh(group1, group2)
        if result == 0:
            return self._find_fake_coin_recursive(group3)
        return self._find_fake_coin_recursive(group1) if result == -1 else self._find_fake_coin_recursive(group2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        keeper = CoinsKeeper()
        keeper.set_n_gen(data['n_gen'])
        keeper.set_n_fake_l(data['n_fake_l'])
        keeper.set_n_fake_g(data['n_fake_g'])
        keeper.set_k_gen(data['k_gen'])
        keeper.set_k_fake_l(data['k_fake_l'])
        keeper.set_k_fake_g(data['k_fake_g'])
        keeper.set_weights(data['weights'])

        keeper.validate()  # Validate data

        detector = CoinsDetector(keeper)
        result = detector.find_fake_coin()
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
