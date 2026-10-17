# Run guide

The [README](README.md#setup) is the maintained setup and usage guide. It covers environment setup, calibration, controls, optional analytics/OpenVINO dependencies, and the timing limitations of prerecorded-video analysis.

From the repository root, the demonstration sequence is:

```bash
python img.py
python se.py
python main.py
python analyze_logs.py
```

Install dependencies first, select `img_0.jpg` in the region selector, and save `bounding_boxes.json` before starting the monitor. The analytics step requires `requirements-analytics.txt` and an existing occupancy log.
