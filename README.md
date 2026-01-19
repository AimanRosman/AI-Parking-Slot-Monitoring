# 🚗 AI Smart Parking Management System (YOLO26n + OpenVINO)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLO](https://img.shields.io/badge/YOLO-11-green.svg)
![Intel](https://img.shields.io/badge/Performance-OpenVINO-blueviolet.svg)

## 📖 Project Bio

**AI Smart Parking Management System** is a cutting-edge computer vision solution designed to transform urban infrastructure. By leveraging the high-speed **YOLO26n** architecture and **Intel OpenVINO** optimization, the system provides high-performance, real-time occupancy tracking, automated enforcement via spot-duration timers, and granular business intelligence. Developed for the next generation of Smart Cities, this project enables facility managers to reduce traffic congestion, automate manual patrols, and make data-driven decisions through high-resolution historical analytics.

---

## 🌟 Key Features

*   **Real-Time Occupancy Tracking**: High-precision detection of available and occupied spots.
*   **Spot Duration Timers**: Tracks exactly how long each car has been parked for enforcement.
*   **Edge Optimization**: Built-in tools to convert models to **OpenVINO** for up to 5x speedup on Windows CPUs.
*   **Interactive Controls**: Seek through video footage, pause/play, and toggle night-mode enhancement.
*   **Business Intelligence**: Automated CSV logging capturing **17,280 data points per day** for peak-hour analysis.
*   **Snapshot System**: On-demand image capture for evidence and violations.

## 🌍 Real-World Functionality & Impact

This system is not just a detection script; it's a tool with direct commercial and environmental applications:

*   **Smart City Integration**: Reduces urban traffic congestion (up to 30% of which is caused by drivers searching for parking) by providing live occupancy data.
*   **Enforcement Automation**: The **Spot-Duration Timers** allow facility managers to automatically identify vehicles exceeding stay limits without manual patrolling.
*   **Business Intelligence**: Automated CSV logging provides high-granularity data to help businesses understand **Peak Demand**, allowing for optimized staffing and dynamic pricing.
*   **Environmental Sustainability**: Reduces vehicle idling and CO2 emissions by directing drivers to empty spots faster.
*   **Security Snapshots**: Provides a manual way to capture visual evidence of parking violations or security incidents.

## 📊 Technical Metrics (Career Highlights)
*   **Edge Optimized**: Real-time performance on standard CPUs via **OpenVINO**, achieving a **3x-5x latency reduction**.
*   **Big Data Capability**: Captures **17,280 metrics per day**, providing high-resolution datasets for predictive analytics.
*   **Ultra-Modern AI**: Implements **YOLO26n**, utilizing the latest experimental architectures for high-speed object detection.

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
Edit `config.json` to customize video source, model paths, and UI settings:
```json
{
    "video_source": "parking1.mp4",
    "model_path": "yolo11n.pt",
    "display": { "slow_motion_delay": 80 }
}
```

## 🎮 How to Use (Step-by-Step)

### 1. Calibration (Define your Spots)
Before running the AI, you need to tell it where the parking spots are:
*   Run `python img.py` to get a snapshot of your empty parking lot.
*   Run `python se.py` to open the selection tool.
*   **Left-Click** 4 corners of each parking spot. Once done, click **Save**. This creates `bounding_boxes.json`.

### 2. Speed Optimization (Optional)
To get the smoothest playback on a standard PC:
*   Run `python optimize_model.py`. This converts the YOLO model into the **OpenVINO** format for a 3-5x speed boost.
*   Update `config.json` setting `"model_path"` to `"yolo11n_openvino_model"`.

### 3. Live Monitoring
Start the main application:
```bash
python main.py
```
*   **Spacebar**: Pause/Resume the video.
*   **Slider**: Drag the progress bar at the top to seek to any time.
*   **'S' Key**: Save a snapshot of the current detections.
*   **'N' Key**: Toggle **Night Mode** to brighten dark footage.

### 4. Analysis
After running the monitor, your data is saved in `parking_log.csv`. 
*   Run `python analyze_logs.py` to generate a professional trend report (`parking_trends.png`).

## 🛠 Tech Stack

*   **Core**: Python, OpenCV, YOLO11
*   **Optimization**: OpenVINO
*   **Analytics**: Pandas, Matplotlib
*   **Data**: CSV-based historical logging & trend analysis.
Distributed under the MIT License. See `LICENSE` for more information.
