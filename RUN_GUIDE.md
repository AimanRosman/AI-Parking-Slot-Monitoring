# Smart Parking Lot AI - Guide

This project monitors parking lot occupancy using YOLO11 and provides data-driven insights.

## 🚀 1. Setup & Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ 2. Configuration

Most settings are managed through `config.json`. You can customize:
- `video_source`: Path to your video file.
- `model_path`: Path to YOLO model (e.g., `yolo11n.pt` or OpenVINO).
- `display`: Window resolution and playback speed (slow-mo).

## 🖱 3. Define Parking Spots

1.  **Extract a reference image**:
    `python img.py`
2.  **Run the selection tool**:
    `python se.py`
3.  **Draw spots**: Select 4 points per spot using your mouse. Click **Save** to update `bounding_boxes.json`.

## 🖥 4. Running the Monitor

Launch the main application:
```bash
python main.py
```

### ⌨️ Keyboard Controls:
- **Spacebar**: Pause / Play
- **Progress Slider**: Drag at the top to seek through video
- **`S` key**: Save a high-quality Snapshot
- **`N` key**: Toggle Night-Mode enhancement
- **ESC**: Exit window

## 📊 5. Data & Analytics

- **Historical Logs**: Occupancy data is saved to `parking_log.csv` every 5 seconds.
- **Trend Charts**: Run `python analyze_logs.py` to generate a trend graph (`parking_trends.png`).
- **Optimization**: Run `python optimize_model.py` to convert the model to OpenVINO for faster playback.
