import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_parking_logs(csv_file="parking_log.csv"):
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Run main.py first to generate logs.")
        return

    # Load data
    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df['Timestamp'], df['Occupied'], label='Occupied Spots', color='red', marker='o')
    plt.plot(df['Timestamp'], df['Available'], label='Available Spots', color='green', marker='x')

    plt.title('Parking Lot Occupancy Trends Over Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Spots')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the graph
    graph_file = "parking_trends.png"
    plt.savefig(graph_file)
    print(f"Success! Analysis saved to {graph_file}")
    plt.show()

if __name__ == "__main__":
    analyze_parking_logs()
