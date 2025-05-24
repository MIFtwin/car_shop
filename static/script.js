
function loadCars(search = '') {
    fetch(`/api/cars?search=${search}`)
        .then(response => response.json())
        .then(cars => {
            carList.innerHTML = '';
            cars.forEach(car => renderCar(car));
        });
}

carForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('brand', document.getElementById('brand').value);
    formData.append('model', document.getElementById('model').value);
    formData.append('year', document.getElementById('year').value);
    formData.append('image', document.getElementById('image').files[0]);

    fetch('/api/cars', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(newCar => {
            loadCars();
            carForm.reset();
        });
});

function searchCars() {
    const search = document.getElementById('searchInput').value;
    loadCars(search);
}

function renderCar(car) {
    const li = document.createElement('li');
    li.innerHTML = `
        <div class="car-info">
            <strong>${car.brand} ${car.model} (${car.year})</strong>
            ${car.image ? `<img src="/static/uploads/${car.image}" width="100">` : ''}
        </div>
        <button onclick="deleteCar(${car.id})">Удалить</button>
    `;
    carList.appendChild(li);
}

function deleteCar(id) {
    fetch(`/api/cars/${id}`, { method: 'DELETE' })
        .then(() => loadCars());
}

document.addEventListener('DOMContentLoaded', () => loadCars());