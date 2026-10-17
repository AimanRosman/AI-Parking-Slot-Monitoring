# AI Parking Slot Monitoring

A desktop computer vision prototype for monitoring parking occupancy in recorded video. It combines YOLO car detection with manually defined parking polygons, displays occupancy and elapsed spot timers, and writes CSV logs for later analysis.

The current configuration and export script use `yolo11n.pt`. Performance and detection accuracy depend on the footage, model, hardware, and calibration; this repository does not include measured accuracy or speedup results.

## What the project demonstrates

- An OpenCV video interface with pause, seek, snapshots, and a brightness enhancement toggle.
- A Tkinter tool for drawing four-corner parking regions.
- Car detection through Ultralytics and occupancy determined by each bounding box's center point falling inside a region.
- Per-region elapsed occupancy timers and a nearly-full overlay.
- Periodic timestamped CSV occupancy records and a Matplotlib trend chart.
- An optional model export path for OpenVINO.

```text
Video -> resized frames -> YOLO detections -> polygon occupancy -> annotated display
                                             |                    `-> snapshots
                                             `-> CSV -> trend chart
```

## Files

| File | Role |
| --- | --- |
| [`main.py`](main.py) | Video interface, configuration, logging, and snapshots |
| [`parking.py`](parking.py) | Region selector and occupancy/timer processing |
| [`config.json`](config.json) | Video/model paths, display, log, and alert settings |
| [`img.py`](img.py) | Extracts a 1080 × 600 calibration frame from `parking1.mp4` |
| [`se.py`](se.py) | Opens the region selector |
| [`optimize_model.py`](optimize_model.py) | Exports `yolo11n.pt` to OpenVINO |
| [`analyze_logs.py`](analyze_logs.py) | Plots occupancy history |
| [`parking1.mp4`](parking1.mp4) | Included demonstration footage |

## Setup

Use a Python environment with a graphical desktop and Tkinter support. Dependency versions are not locked, and `parking.py` imports Ultralytics internal solution APIs, so compatibility must be checked against the installed release.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

For trend charts, also install the optional analytics dependencies:

```bash
python -m pip install -r requirements-analytics.txt
```

Run all commands from the repository root; file paths are relative to the working directory.

## Calibrate and run

1. Review `config.json`. The default input is `parking1.mp4`, model is `yolo11n.pt`, region file is `bounding_boxes.json`, and display size is 1080 × 600.
2. Run `python img.py` to extract `img_0.jpg` from the bundled video. For another input, update the hard-coded video path in `img.py`; it does not read `config.json`.
3. Run `python se.py`, choose **Upload Image**, and open `img_0.jpg`.
4. Click the four corners of each parking space in perimeter order. Use **Remove Last BBox** to undo and **Save** to create `bounding_boxes.json`.
5. Start the monitor:

```bash
python main.py
```

Keep the calibration image dimensions equal to the processing dimensions in `config.json`. The selector saves coordinates in the uploaded image's original coordinate system, while the monitor resizes video frames before detection.

Model weights are not committed; Ultralytics may download a recognized model on first use. Use weights from a trusted source.

| Control | Action |
| --- | --- |
| Space | Pause or resume |
| Progress slider | Seek within the video |
| `s` | Save `snapshot_<timestamp>.jpg` |
| `n` | Toggle brightness/contrast enhancement |
| Escape or close window | Exit |

The video loops automatically. A snapshot contains the annotated frame and may contain identifiable people or number plates.

## Configuration and outputs

| Setting | Purpose |
| --- | --- |
| `video_source`, `model_path`, `json_file` | Input video, detector, and calibration paths |
| `display.width`, `display.height` | Processing image size; must match calibration |
| `display.slow_motion_delay` | Milliseconds passed to OpenCV key polling, in addition to processing time |
| `display.show_fps`, `display.show_status` | Display overlays |
| `logging.enabled`, `interval_seconds`, `csv_file` | Wall-clock log interval and destination |
| `alerts.nearly_full_threshold` | Available-space threshold for the overlay |
| `alerts.overstay_seconds` | Present in configuration, but not used by the current code |

When logging is enabled, `parking_log.csv` records `Timestamp`, `Occupied`, and `Available`. With data available, run:

```bash
python analyze_logs.py
```

This writes `parking_trends.png` and opens the chart window.

For optional OpenVINO export, install `openvino`, run `python optimize_model.py`, and set `config.json`'s `model_path` to the returned export directory, typically `yolo11n_openvino_model`. Check the exported model against the same footage before relying on it; there is no benchmark proving a particular speed improvement.

## Limitations and validation

- Detection is restricted to class `2` (cars). Occlusion, camera movement, overlapping regions, and non-car vehicles can affect counts.
- Timers measure elapsed wall-clock time while a region is occupied. They are not vehicle identities and do not reset when seeking or looping video; they should not be used as enforcement evidence.
- CSV timestamps also use wall-clock time rather than video timestamps. Playback speed and pause behavior affect the resulting log.
- The UI assumes a seekable input with a frame count; live streams are not validated.
- There is no committed calibration file, automated test suite, pinned environment, or evaluation dataset. Confirm calibration, empty/occupied counts, pause/seek/loop behavior, and CSV/chart output on your own footage before a demonstration.
- Keep private footage, generated snapshots, and site-specific logs out of public commits. `.gitignore` excludes generated outputs but cannot remove previously committed data.

## License

See the [MIT License](LICENSE). Review the separate terms for Ultralytics, model weights, and any footage you use.
