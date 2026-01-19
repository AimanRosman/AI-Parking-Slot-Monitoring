import cv2
import json

from parking import ParkingManagement

# Load Configuration
with open("config.json", "r") as f:
    config = json.load(f)

# Video capture
cap = cv2.VideoCapture(config["video_source"])




# Initialize parking management object
parking_manager =  ParkingManagement(
    model=config["model_path"],
    classes=[2],
    json_file=config["json_file"],
)

import time
import csv
from datetime import datetime
import os

prev_time = 0
log_interval = config["logging"]["interval_seconds"]
last_log_time = 0
csv_file = config["logging"]["csv_file"]
peak_occupied = 0

# Initialize CSV file if it doesn't exist
if config["logging"]["enabled"] and not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Occupied", "Available"])

# Window setup for trackbar
window_name = "Parking Detection"
cv2.namedWindow(window_name)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cv2.createTrackbar("Progress", window_name, 0, total_frames - 1, lambda x: None)

paused = False
im0_processed = None # Cache for the processed frame
night_mode = False

while cap.isOpened():
    # 1. Check if user moved the trackbar (Seeking)
    trackbar_pos = cv2.getTrackbarPos("Progress", window_name)
    current_frame_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    
    # If the trackbar is moved manually (not by the code)
    if abs(trackbar_pos - current_frame_pos) > 2:
        cap.set(cv2.CAP_PROP_POS_FRAMES, trackbar_pos)
        im0_processed = None # Force re-process on seek

    # 2. Grab a frame if playing or if we need a refresh (seek/start)
    if not paused or im0_processed is None:
        ret, im0 = cap.read()
        if not ret:
            # Auto-loop: reset to the beginning of the video
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, im0 = cap.read()
            if not ret: break # Break if video still can't be read

        # Update trackbar position to follow video
        cv2.setTrackbarPos("Progress", window_name, int(cap.get(cv2.CAP_PROP_POS_FRAMES)))

        # Process the frame
        im01 = cv2.resize(im0, (config["display"]["width"], config["display"]["height"]))
        
        # Apply Night Mode Enhancement if enabled
        if night_mode:
            # Increase brightness and contrast
            im01 = cv2.convertScaleAbs(im01, alpha=1.5, beta=30)
            cv2.putText(im01, "NIGHT MODE ACTIVE", (config["display"]["width"] - 230, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        im0_processed = parking_manager.process_data(im01)

        # UI Stats
        if config["display"]["show_status"]:
            occupied = parking_manager.pr_info.get("Occupancy", 0)
            available = parking_manager.pr_info.get("Available", 0)
            
            # Track peak occupancy
            if occupied > peak_occupied:
                peak_occupied = occupied
                
            if available <= config["alerts"]["nearly_full_threshold"]: # Warning when 2 or fewer spots left
                cv2.putText(im0_processed, "LOT NEARLY FULL!", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            status_text = "PAUSED" if paused else "PLAYING"
            cv2.putText(im0_processed, status_text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if paused else (0, 255, 0), 2)
            cv2.putText(im0_processed, f"Peak Today: {peak_occupied}", (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)

        # FPS
        if config["display"]["show_fps"]:
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
            prev_time = curr_time
            cv2.putText(im0_processed, f"FPS: {fps:.2f}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 5. Log occupancy data periodically
        if config["logging"]["enabled"] and (time.time() - last_log_time > log_interval):
            occupied = parking_manager.pr_info.get("Occupancy", 0)
            available = parking_manager.pr_info.get("Available", 0)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, occupied, available])
            last_log_time = time.time()

    # 3. Always show the last (or newly) processed frame
    cv2.imshow(window_name, im0_processed)
    
    # 3.5 Check if window was closed manually
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

    # 4. Handle keys
    key = cv2.waitKey(config["display"]["slow_motion_delay"]) & 0xFF
    if key == 27: # ESC to quit
        break
    elif key == ord(' '): # Space to pause/play
        paused = not paused
    elif key == ord('s') or key == ord('S'): # S for Snapshot
        snapshot_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f"snapshot_{snapshot_time}.jpg", im0_processed)
        print(f"📸 Snapshot saved as snapshot_{snapshot_time}.jpg")
    elif key == ord('n') or key == ord('N'): # N for Night Mode
        night_mode = not night_mode
cap.release()
cv2.destroyAllWindows()