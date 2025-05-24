from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

cars = [
    {"id": 1, "brand": "Toyota", "model": "Camry", "year": 2020},
    {"id": 2, "brand": "BMW", "model": "X5", "year": 2019}
]

class CarDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.brand = data.get("brand")
        self.model = data.get("model")
        self.year = data.get("year")

@app.route('/api/cars', methods=['GET'])
def get_cars():
    return jsonify(cars)

@app.route('/api/cars', methods=['POST'])
def add_car():
    new_car = request.json
    new_car["id"] = len(cars) + 1
    cars.append(new_car)
    return jsonify(new_car), 201

@app.route('/api/cars/<int:id>', methods=['PUT'])
def update_car(id):
    car = next((c for c in cars if c["id"] == id), None)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    data = request.json
    car.update(data)
    return jsonify(car)

@app.route('/api/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    global cars
    cars = [c for c in cars if c["id"] != id]
    return jsonify({"message": "Car deleted"}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)