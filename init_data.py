import csv
import os

def init_sensor_data():
    csv_file = 'sensor_data.csv'
    headers = [
        'Timestamp', 'IR', 'Red', 'HeartRate', 'SpO2',
        'AccelX', 'AccelY', 'AccelZ', 'GyroX', 'GyroY',
        'GyroZ', 'Temp', 'GSR', 'Cortisol', 'StressLevel'
    ]
    
    # Create fresh CSV file with headers
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        # Add some sample data
        writer.writerow([
            '2024-03-06 12:00:00', 100, 200, 75, 98,
            0, 0, 0, 0, 0, 0, 37, 500, 12.5, 'Medium'
        ])
    
    print(f"Created {csv_file} with headers and sample data")

if __name__ == "__main__":
    init_sensor_data()
