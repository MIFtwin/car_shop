document.addEventListener('DOMContentLoaded', () => {
    const carForm = document.getElementById('carForm');
    const carList = document.getElementById('carList');

    fetch('/api/cars')
        .then(response => response.json())
        .then(cars => {
            cars.forEach(car => renderCar(car));
        });

    carForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const car = {
            brand: document.getElementById('brand').value,
            model: document.getElementById('model').value,
            year: parseInt(document.getElementById('year').value)
        };
        fetch('/api/cars', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(car)
        })
            .then(response => response.json())
            .then(newCar => {
                renderCar(newCar);
                carForm.reset();
            });
    });

    function renderCar(car) {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${car.brand} ${car.model} (${car.year})</span>
            <button onclick="deleteCar(${car.id})">Удалить</button>
        `;
        carList.appendChild(li);
    }
});

function deleteCar(id) {
    fetch(`/api/cars/${id}`, { method: 'DELETE' })
        .then(() => {
            window.location.reload();
        });
}