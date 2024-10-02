function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            var url = 'https://api.waqi.info/feed/geo:' + latitude + ';' + longitude + '/?token=7f1bf3b5bb58aa3dc9b043c7d4c5d299cdd565a5';

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    var pollutants = data.data.iaqi;
                    document.getElementById("latitude").value = latitude.toFixed(6);
                    document.getElementById("longitude").value = longitude.toFixed(6);
                    document.getElementById("city").value = data.data.city.name;
                    document.getElementById("PM2.5").value = pollutants.pm25 ? pollutants.pm25.v : '';
                    document.getElementById("PM10").value = pollutants.pm10 ? pollutants.pm10.v : '';
                    document.getElementById("O3").value = pollutants.o3 ? pollutants.o3.v : '';
                    document.getElementById("NO2").value = pollutants.no2 ? pollutants.no2.v : '';
                    document.getElementById("SO2").value = pollutants.so2 ? pollutants.so2.v : '';
                    document.getElementById("CO").value = pollutants.co ? pollutants.co.v : '';
                })
                .catch(error => {
                    console.error('Error fetching air quality data:', error);
                });
        }, function () {
            console.error('Geolocation error: User denied the request for Geolocation.');
        });
    } else {
        console.error('Geolocation error: Geolocation is not supported by this browser.');
    }
}

// Chart.js example
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'AQI Levels',
            data: [12, 19, 3, 5, 2, 3, 9],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
