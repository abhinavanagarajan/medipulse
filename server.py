from flask import Flask, request
import csv
import requests
import prediction
from datetime import datetime

app = Flask(__name__)

CHANNEL_ID = "2812750"  # ThingSpeak Channel ID
FIELD_NUMBER = "1"  # Field number to fetch data from
READ_API_KEY = "GOK6A3Q24ISSDTT1"  # Read API Key
WRITE_API_KEY = "EKUIJFY8GJB154L5"  # Replace with your Write API Key
READ_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD_NUMBER}.json?results=10&api_key={READ_API_KEY}"
WRITE_URL = f"https://api.thingspeak.com/update"


@app.route('/log', methods=['POST'])
def log_data():
    data = request.json

    #The API endpoint
    url = "http://192.168.214.148:5500/sensor_data"

    # Data to be sent
    data_tosms = {
        "sensor_values": [data.get("IR"), 
        data.get("Red"), 
        data.get("HeartRate"),
        data.get("GSR")]
    }
    
    model_file = "physiological_data_model_20250306_163919.joblib"
    scaler_file = "physiological_data_scaler_20250306_163919.joblib"
    features_file = "physiological_data_features_20250306_163919.joblib"
    
    # Load the saved model and associated files
    model, scaler, features = prediction.load_saved_model(model_file, scaler_file, features_file)
    avg_value=prediction.predict_with_model(model, scaler, [data.get("IR"), data.get("Red"), data.get("HeartRate"),data.get("GSR")], features)
    send_data(data.get("GSR"),data.get("HeartRate"),avg_value)
    #send_data(data.get("Cortisol"),3)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("sensor_data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, data.get("IR"), data.get("Red"), 
                         data.get("HeartRate"), data.get("SpO2"), 
                         data.get("AccelX"), data.get("AccelY"), data.get("AccelZ"),
                         data.get("GyroX"), data.get("GyroY"), data.get("GyroZ"),
                         data.get("Temp"), data.get("GSR")])

    return "Logged", 200

def send_data(val1,val2,val3):
    """Send data to ThingSpeak."""
    
    payload = {
        "api_key": WRITE_API_KEY,
        f"field1": val1,
        f"field2": val2,
        f"field3": val3
    }
    response = requests.post(WRITE_URL, params=payload)
    if response.status_code == 200:
        print(f"Data sent: {val1}, {val2}")
    else:
        print("Failed to send data", response.text)
    # A POST request to the API

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
