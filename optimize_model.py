from ultralytics import YOLO
import torch

def optimize_for_cpu():
    print("🚀 Starting optimization for Windows CPU...")
    
    # Load the standard Nano model
    model_name = "yolo11n.pt"
    model = YOLO(model_name)
    
    print(f"📦 Exporting {model_name} to OpenVINO format (this may take a minute)...")
    
    # Export the model
    # OpenVINO is the best format for Intel/AMD CPUs on Windows
    # It provides up to 3x-5x faster inference than standard .pt files
    try:
        export_path = model.export(format="openvino")
        print(f"\n✅ SUCCESS! Model exported to: {export_path}")
        print("\n🔧 TO USE THIS OPTIMIZED MODEL:")
        print("1. Open main.py")
        print(f"2. Change model='{model_name}' to model='yolo11n_openvino_model'")
        print("3. Run python main.py")
    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        print("Make sure you have openvino installed: pip install openvino")

if __name__ == "__main__":
    optimize_for_cpu()
