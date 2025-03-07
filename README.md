# MediPulse - AI-Powered Healthcare Platform

## **Introduction**
MediPulse is an **AI-powered healthcare platform** designed for real-time monitoring, prediction, and management of stress, anxiety, trauma, and post-traumatic stress disorder (PTSD). It utilizes **biometric sensors, machine learning models, and adaptive relaxation techniques** to assist patients, caregivers, and healthcare professionals in proactive stress management.

MediPulse ensures **secure guardian access**, real-time alerts, and **automated notifications** when stress levels exceed safe thresholds. Additionally, it features an **AI-driven chatbot** and **personalized therapy recommendations** to improve mental well-being.

---
## **Key Features**
### **1. Real-Time Biometric Monitoring**
- **Sensors Used:**
  - **MAX30102** - Heart Rate, IR, Red Light, SpO2
  - **GSR (Galvanic Skin Response)** - Skin Conductance
  - **Temperature Sensor** - Body Temperature
- **Data Processing:**
  - Sensor data is transmitted via **ESP32 (WiFi Module)** to a local storage server.
  - Real-time visualization through a **Flask-based WebApp**.

### **2. AI-Based Cortisol Prediction**
- **Machine Learning Model** trained on biometric data to predict **cortisol levels** (Low, Medium, High).
- Live monitoring dashboard updates stress levels dynamically.

### **3. Automated Alerts & Secure Guardian Access**
- **Threshold-Based Alerts:**
  - If cortisol levels exceed the threshold, **instant notifications** are sent via **Twilio API** to designated caregivers, doctors, or NGOs.
- **Guardian Dashboard:**
  - Secure access for authorized caregivers to monitor patient health trends.

### **4. AI-Powered Chatbot for Mental Health**
- **Custom LLM Chatbot using Google Gemini API**
- Engages patients with:
  - Mindfulness exercises
  - Guided breathing techniques
  - Supportive and empathetic conversations
- Helps patients **cope with stress, anxiety, and overthinking**.

### **5. Adaptive Relaxation Techniques**
- Personalized **stress relief activities** based on AI-predicted cortisol levels:
  - **Low Stress:** Soothing Music, Guided Meditation
  - **Medium Stress:** Yoga, Breathing Exercises
  - **High Stress:** Simple Mind Games, Emergency Interventions
- Pop-up recommendations ensure **instant relief**.

### **6. Comprehensive Health Reports & Insights**
- **Automated 30-Day Report Generation**
  - Tracks **cortisol trends, stress frequency, and threshold breaches**.
  - Exports as **PDF** for doctors & caregivers.

### **7. Self-Harm Prevention & Rehabilitation Support**
- **High-risk patients are monitored closely** to prevent self-harm.
- Notifications sent to **rehabilitation centers** for immediate intervention.
- Educates patients on **mental health, trauma awareness, and coping mechanisms**.

---
## **Technology Stack**
| Component               | Technology Used  |
|------------------------|----------------|
| **Microcontroller**    | ESP32 (WiFi)   |
| **Sensors**           | MAX30102, GSR, SpO2, Temperature Sensor |
| **Data Transmission** | WiFi Communication to Local Server |
| **Machine Learning**  | Custom ML Model (Cortisol Prediction) |
| **Backend**          | Python (Flask) |
| **Frontend**         | HTML, CSS, JavaScript |
| **Messaging API**    | Twilio API for alerts |
| **AI Chatbot**       | Google Gemini API + Custom LLM |
| **Storage**          | Local Server + CSV/Database |
| **Report Generation** | Python (PDF Generation) |

---
## **System Workflow**
1. **Data Collection:** Sensors (MAX30102, GSR, SpO2, Temperature) collect real-time patient data.
2. **Data Processing:** Data is transmitted via ESP32 and stored on a local server.
3. **Cortisol Prediction:** ML model processes the data and classifies stress levels.
4. **Live Visualization:** Flask-based WebApp displays real-time metrics.
5. **Alert System:** If stress exceeds AI-defined thresholds, Twilio sends notifications.
6. **Chatbot Assistance:** Patients engage with the chatbot for stress relief techniques.
7. **Adaptive Therapy:** Based on detected stress levels, patients receive relaxation recommendations.
8. **Report Generation:** A 30-day cortisol trend report is generated for analysis.
9. **Rehabilitation & Self-Harm Prevention:** High-risk cases trigger notifications to rehab centers.

---
## **Installation & Deployment**
### **1. Prerequisites**
- Python 3.8+
- Flask
- Twilio API Key
- Google Gemini API Key
- ESP32 Microcontroller
- Sensors (MAX30102, GSR, SpO2, Temperature)

### **2. Clone the Repository**
```bash
   git clone https://github.com/your-repo/medipulse.git
   cd medipulse
```

### **3. Install Dependencies**
```bash
   pip install flask pandas numpy tensorflow twilio
```

### **4. Run the Flask WebApp**
```bash
   python app.py
```

### **5. Configure ESP32 Data Transmission**
- Upload Arduino code for **ESP32** to stream data to the Flask server.
- Set WiFi credentials for ESP32 to transmit readings.

### **6. Deploy the ML Model**
- Train and integrate the **cortisol prediction model**.
- Ensure model inference is optimized for real-time predictions.

---
## **Future Enhancements**
- **Cloud Storage & IoT Integration** for remote monitoring.
- **Mobile App Development** for increased accessibility.
- **Voice-Based AI Assistance** for stress relief.
- **Expanded Therapy Options** including **VR relaxation techniques**.

---
## **Contributors**
- **Abhinavanagarajan A** 
- **Vishnu Swaroop G**
- **Smitha Gladius TS**
- **Swetha S**

---
## **License**
MediPulse is an open-source project licensed under **MIT License**. Feel free to contribute and improve the platform.


