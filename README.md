# GeoWatch Tower

**GeoWatch Tower** is a real-time AI-powered monitoring system designed to track, analyze, and detect anomalous behaviors across geographical locations. It leverages behavioral data, geolocation intelligence, and machine learning techniques to identify suspicious patterns, making it an ideal solution for security monitoring, bot detection, and threat reconnaissance.

---
![GeoWatch Tower](https://github.com/user-attachments/assets/9777a545-bd31-4bf7-905d-7a595eb446fb)

---

## Features

- **Real-Time Geolocation Tracking**: Monitors incoming data streams and maps activities based on IP geolocation.
- **Anomaly Detection**: Uses ML models to detect suspicious behavioral patterns and geographic anomalies.
- **Behavioral Analytics**: Tracks usage patterns, interactions, and frequency to model normal vs. abnormal behaviors.
- **Visualization**: Provides interactive dashboards for monitoring system status and alerts.
- **Alert Mechanism**: Triggers alerts upon detection of potential threats or suspicious movement patterns.

---

## Core Technologies

- Python 3.10+
- TensorFlow / Scikit-learn (for ML models)
- GeoIP2 / Geopy (for geolocation)
- Streamlit (for dashboard visualization)
- Pandas, NumPy (for data handling)
- Matplotlib, Seaborn (for plotting)

---

## Setup Instructions

1. **Clone the Repository**

```bash
git clone "https://github.com/SakaethRam/GeoWatchTower.git"
cd GeoWatchTower
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the Application**

```bash
streamlit run app.py
```

4. **Build and Run with Docker**

To build the Docker image:

```bash
docker build -t geowatch-tower .
```

To run the Docker container:

```bash
docker run -p 8501:8501 geowatch-tower
```

## Project Structure

```
GeoWatch-Tower/
├── data/                 # Raw and processed datasets
├── models/               # Saved ML models
├── notebooks/            # Development and experimentation notebooks
├── src/                  # Source code for data processing, modeling, visualization
├── app.py                # Main entry point (Streamlit app)
├── requirements.txt      # List of project dependencies
├── Dockerfile            # Docker configuration file
└── README.md             # Project documentation
```

---

## How It Works

1. **Data Collection**: The system ingests data with IP addresses and timestamps.
2. **Geolocation Mapping**: IP addresses are mapped to geographical coordinates.
3. **Behavioral Modeling**: Patterns are learned over time to build a normal behavioral baseline.
4. **Anomaly Detection**: Incoming activities are analyzed against the baseline to detect deviations.
5. **Visualization & Alerts**: Deviations are visualized, and alerts are generated for critical anomalies.

## Use Cases

- Cybersecurity monitoring
- Social network bot detection
- Fraudulent activity detection
- Network anomaly analysis

---

## Contribution

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request. Ensure that all code is properly documented and tested.

### Contribution Guidelines

To contribute:

- Fork the repository.
- Create a feature branch.
- Implement your changes.
- Submit a pull request with a clear description of modifications.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

For questions, collaboration, or further support, please contact the project maintainer at [sakaethrambusiness@gmail.com].

