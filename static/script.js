// Initialize charts
let heartRateChart, gsrChart, cortisolChart;
const maxDataPoints = 50;

function initializeCharts() {
    const commonOptions = {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second'
                }
            },
            y: {
                beginAtZero: true
            }
        },
        animation: false,
        responsive: true,
        maintainAspectRatio: false
    };

    heartRateChart = new Chart('heartRateChart', {
        type: 'line',
        data: {
            datasets: [{
                label: 'Heart Rate (BPM)',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.4
            }]
        },
        options: commonOptions
    });

    gsrChart = new Chart('gsrChart', {
        type: 'line',
        data: {
            datasets: [{
                label: 'GSR Value',
                data: [],
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.4
            }]
        },
        options: commonOptions
    });

    cortisolChart = new Chart('cortisolChart', {
        type: 'line',
        data: {
            datasets: [{
                label: 'Cortisol Level (μg/dL)',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.4
            }]
        },
        options: commonOptions
    });
}

function updateCharts(data) {
    const timestamp = new Date(data.Timestamp);

    // Update Heart Rate
    heartRateChart.data.datasets[0].data.push({
        x: timestamp,
        y: data.HeartRate
    });
    if (heartRateChart.data.datasets[0].data.length > maxDataPoints) {
        heartRateChart.data.datasets[0].data.shift();
    }
    heartRateChart.update();

    // Update GSR
    gsrChart.data.datasets[0].data.push({
        x: timestamp,
        y: data.GSR
    });
    if (gsrChart.data.datasets[0].data.length > maxDataPoints) {
        gsrChart.data.datasets[0].data.shift();
    }
    gsrChart.update();

    // Update Cortisol
    cortisolChart.data.datasets[0].data.push({
        x: timestamp,
        y: data.predicted_cortisol
    });
    if (cortisolChart.data.datasets[0].data.length > maxDataPoints) {
        cortisolChart.data.datasets[0].data.shift();
    }
    cortisolChart.update();

    // Update Cortisol Display
    document.getElementById('cortisolValue').textContent = 
        data.predicted_cortisol.toFixed(2);
    document.getElementById('cortisolClass').textContent = 
        data.stress_classification;
}

function fetchLiveData() {
    fetch('/live-data')
        .then(response => response.json())
        .then(data => updateCharts(data))
        .catch(error => console.error('Error fetching data:', error));
}

function downloadReport() {
    window.location.href = '/download-report';
}

// Initialize charts when page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    // Fetch data every second
    setInterval(fetchLiveData, 1000);
});
