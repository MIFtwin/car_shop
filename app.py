from flask import Flask, jsonify, request, render_template, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

cars = [
    {"id": 1, "brand": "Toyota", "model": "Camry", "year": 2020, "image": None},
    {"id": 2, "brand": "BMW", "model": "X5", "year": 2019, "image": None}
]

@app.route('/api/cars', methods=['GET'])
def get_cars():
    search = request.args.get('search')
    if search:
        filtered = [c for c in cars if search.lower() in c["brand"].lower() or 
                   search.lower() in c["model"].lower()]
        return jsonify(filtered)
    return jsonify(cars)

@app.route('/api/cars', methods=['POST'])
def add_car():
    data = request.form
    image = request.files.get('image')
    
    new_car = {
        "id": len(cars) + 1,
        "brand": data.get("brand"),
        "model": data.get("model"),
        "year": int(data.get("year")),
        "image": None
    }
    
    if image:
        filename = f"car_{new_car['id']}.jpg"
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_car["image"] = filename
    
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

@app.route('/static/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)