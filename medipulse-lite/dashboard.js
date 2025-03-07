let allLabels = [];
let allHeartRateData = [];
let allGsrData = [];
let allCortisolData = [];
let startIndex = 0;  // Start at index 0
const shiftSize = 1; // Move by 1 reading per update
const windowSize = 70; // Show 70 readings at a time

function loadCSV() {
    const fileInput = document.getElementById('csvFileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            parseCSV(event.target.result);
        };
        reader.readAsText(file);
    } else {
        alert("Please select a CSV file.");
    }
}

function parseCSV(csvData) {
    const rows = csvData.trim().split('\n').slice(1); // Skip header row

    allLabels = [];
    allHeartRateData = [];
    allGsrData = [];
    allCortisolData = [];

    rows.forEach((row, index) => {
        const columns = row.split(',').map(value => value.trim());
        if (columns.length === 7) {
            allLabels.push(`Reading ${index + 1}`);
            allHeartRateData.push(parseFloat(columns[2])); // Heart Rate
            allGsrData.push(parseFloat(columns[3]));       // GSR
            allCortisolData.push(parseFloat(columns[6]));  // Cortisol
        }
    });

    startAutoUpdate();
}

function getWindowData() {
    const endIndex = Math.min(startIndex + windowSize, allLabels.length);
    return {
        labels: allLabels.slice(startIndex, endIndex),
        heartRateData: allHeartRateData.slice(startIndex, endIndex),
        gsrData: allGsrData.slice(startIndex, endIndex),
        cortisolData: allCortisolData.slice(startIndex, endIndex)
    };
}

// Initialize Charts
const ctxHeartRate = document.getElementById('heartRateChart').getContext('2d');
const ctxGsr = document.getElementById('gsrChart').getContext('2d');
const ctxCortisol = document.getElementById('cortisolChart').getContext('2d');

const chartOptions = {
    responsive: true,
    animation: { duration: 500, easing: 'linear' }, // Smooth transition
    elements: { line: { tension: 0.4 } }, // Curve the lines
    scales: {
        x: { title: { display: true, text: "Time" } },
        y: { title: { display: true, text: "Value" } }
    }
};

const heartRateChart = new Chart(ctxHeartRate, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: "Heart Rate (BPM)",
            borderColor: "red",
            backgroundColor: "rgba(255, 0, 0, 0.2)",
            data: [],
            fill: true,
            tension: 0.4
        }]
    },
    options: chartOptions
});

const gsrChart = new Chart(ctxGsr, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: "GSR (µS)",
            borderColor: "blue",
            backgroundColor: "rgba(0, 0, 255, 0.2)",
            data: [],
            fill: true,
            tension: 0.4
        }]
    },
    options: chartOptions
});

const cortisolChart = new Chart(ctxCortisol, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: "Cortisol (µg/dL)",
            borderColor: "purple",
            backgroundColor: "rgba(128, 0, 128, 0.2)",
            data: [],
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        animation: { duration: 500, easing: 'linear' },
        elements: { line: { tension: 0.4 } },
        scales: {
            x: { title: { display: true, text: "Time" } },
            y: { title: { display: true, text: "Cortisol Level" }, min: 0, max: 2 } // Fixed Y-Axis for Cortisol
        }
    }
});

function updateCharts() {
    const { labels, heartRateData, gsrData, cortisolData } = getWindowData();

    heartRateChart.data.labels = labels;
    heartRateChart.data.datasets[0].data = heartRateData;
    heartRateChart.update('none'); // Prevent instant refresh, make it smooth

    gsrChart.data.labels = labels;
    gsrChart.data.datasets[0].data = gsrData;
    gsrChart.update('none');

    cortisolChart.data.labels = labels;
    cortisolChart.data.datasets[0].data = cortisolData;
    cortisolChart.update('none');
}

function startAutoUpdate() {
    setInterval(() => {
        if (startIndex + windowSize < allLabels.length) {
            startIndex += shiftSize; // Move the window forward smoothly by 1 reading
        } else {
            startIndex = 0; // Loop back to start if we reach the end
        }
        updateCharts();
    }, 500); // Update every 500ms for smooth movement
}
