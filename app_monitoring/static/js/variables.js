// indicators.js

document.addEventListener('DOMContentLoaded', function () {
    // Adaptamos layoutConfig para Chart.js
    const layoutConfig = (title, yAxisTitle) => ({
        plugins: {
            title: {
                display: true,
                text: title
            },
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 10
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Tiempo'
                }
            },
            y: {
                title: {
                    display: true,
                    text: yAxisTitle
                },
                beginAtZero: true
            }
        },
        responsive: true,
        maintainAspectRatio: false
    });

    // Configuración de los gráficos
    const chartsConfig = [
        {
            canvasId: 'chart1',
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Dx',
                        data: [],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Dy',
                        data: [],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Dz',
                        data: [],
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: layoutConfig('Gráfico del Magnetómetro', 'Medidas (uT)')
        },
        {
            canvasId: 'chart2',
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Presión atmosférica',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: layoutConfig('Gráfico de Barómetro', 'Presión (hPa)')
        },
        {
            canvasId: 'chart3',
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Decibelios',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: layoutConfig('Gráfico de Ruido', 'Nivel (dB)')
        },
        {
            canvasId: 'chart4',
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Dx',
                        data: [],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Dy',
                        data: [],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Dz',
                        data: [],
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: layoutConfig('Gráfico de Giroscopio', 'Velocidad angular (°/s)')
        },
        {
            canvasId: 'chart5',
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Dx',
                        data: [],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Dy',
                        data: [],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Dz',
                        data: [],
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: layoutConfig('Gráfico de Acelerómetro', 'Aceleración (m/s²)')
        },
        {
            canvasId: 'chart6',
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Vibración',
                    data: [],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: layoutConfig('Gráfico de Vibración', 'Amplitud (mm/s)')
        }
    ];

    // Inicializar los gráficos
    const charts = chartsConfig.map(config => {
        const ctx = document.getElementById(config.canvasId).getContext('2d');
        return new Chart(ctx, {
            type: config.type,
            data: config.data,
            options: config.options
        });
    });

    // Definir la cantidad máxima de puntos de datos
    const MAX_DATA_POINTS = 10;

    // Función para obtener datos desde la API de Django
    function fetchGetData() {
        fetch(GET_LATEST_SENSOR_DATA_URL)
            .then(response => response.json())
            .then(data => {
                updateCharts(data);
            })
            .catch(error => console.error('Error al obtener datos históricos:', error));
    }

    // Variable para simular el tiempo (puedes reemplazar esto con un timestamp real si lo tienes)
    let i = 0;

    // Función para actualizar los gráficos con los datos obtenidos
    function updateCharts(data) {
        i += 1;
        const timeLabel = (i / 60).toFixed(3); // Simular tiempo en segundos

        charts.forEach((chart, index) => {
            // Añadir el nuevo label de tiempo
            chart.data.labels.push(timeLabel);

            // Obtener los datos correspondientes
            switch(index) {
                case 0: // Magnetómetro
                    chart.data.datasets.forEach((dataset, dsIndex) => {
                        const key = ['x', 'y', 'z'][dsIndex];
                        dataset.data.push(data.magnetometro[key]);
                    });
                    break;
                case 1: // Barómetro
                    chart.data.datasets[0].data.push(data.barometro);
                    break;
                case 2: // Ruido
                    chart.data.datasets[0].data.push(data.ruido);
                    break;
                case 3: // Giroscopio
                    chart.data.datasets.forEach((dataset, dsIndex) => {
                        const key = ['x', 'y', 'z'][dsIndex];
                        dataset.data.push(data.giroscopio[key]);
                    });
                    break;
                case 4: // Acelerómetro
                    chart.data.datasets.forEach((dataset, dsIndex) => {
                        const key = ['x', 'y', 'z'][dsIndex];
                        dataset.data.push(data.acelerometro[key]);
                    });
                    break;
                case 5: // Vibración
                    chart.data.datasets[0].data.push(data.vibracion);
                    break;
                default:
                    break;
            }

            // Eliminar el dato más antiguo si se supera el máximo de puntos de datos
            if (chart.data.labels.length > MAX_DATA_POINTS) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(dataset => dataset.data.shift());
            }

            // Actualizar el gráfico
            chart.update();
        });
    }

    // Inicializar la primera llamada para evitar esperar el primer intervalo
    fetchGetData();

    // Configurar el intervalo de actualización usando la variable de Django
    setInterval(fetchGetData, UPDATE_INTERVAL);
});
