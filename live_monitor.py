import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from datetime import datetime
import threading

class SensorMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Sensor Monitor")
        self.root.geometry("1000x800")
        
        # Setup data storage
        self.timestamps = []
        self.heart_rates = []
        self.gsr_values = []
        self.max_points = 100
        
        # Setup UI
        self.setup_ui()
        
        # Start monitoring thread
        self.running = True
        self.monitor_thread = threading.Thread(target=self.update_data, daemon=True)
        self.monitor_thread.start()

    def setup_ui(self):
        # Create main frame
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(sticky="nsew")
        
        # Create value displays
        self.hr_var = tk.StringVar(value="Heart Rate: -- BPM")
        self.gsr_var = tk.StringVar(value="GSR: -- μS")
        
        ttk.Label(self.frame, textvariable=self.hr_var, font=('Arial', 20)).grid(row=0, column=0, pady=10)
        ttk.Label(self.frame, textvariable=self.gsr_var, font=('Arial', 20)).grid(row=0, column=1, pady=10)
        
        # Setup matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        # Configure plots
        for ax, title, color in [(self.ax1, 'Heart Rate (BPM)', 'red'),
                               (self.ax2, 'GSR Value', 'blue')]:
            ax.set_title(title)
            ax.grid(True)
            ax.set_facecolor('#f0f0f0')
        
        self.fig.tight_layout(pad=3.0)

    def update_data(self):
        """Read current sensor data and update plots"""
        while self.running:
            try:
                with open('current_sensor_data.txt', 'r') as f:
                    timestamp, hr, gsr = f.read().strip().split(',')
                    
                    # Update data lists
                    self.timestamps.append(timestamp)
                    self.heart_rates.append(float(hr))
                    self.gsr_values.append(float(gsr))
                    
                    # Keep fixed window of points
                    if len(self.timestamps) > self.max_points:
                        self.timestamps.pop(0)
                        self.heart_rates.pop(0)
                        self.gsr_values.pop(0)
                    
                    # Update display values
                    self.hr_var.set(f"Heart Rate: {hr} BPM")
                    self.gsr_var.set(f"GSR: {gsr} μS")
                    
                    # Update plots
                    self.update_plots()
                    
            except Exception as e:
                print(f"Error updating data: {e}")
            
            time.sleep(0.1)

    def update_plots(self):
        """Update both plots with new data"""
        try:
            # Clear previous plots
            self.ax1.clear()
            self.ax2.clear()
            
            # Plot new data
            self.ax1.plot(self.timestamps, self.heart_rates, 'r-')
            self.ax2.plot(self.timestamps, self.gsr_values, 'b-')
            
            # Configure axes
            for ax in [self.ax1, self.ax2]:
                ax.grid(True)
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            self.ax1.set_title('Heart Rate over Time')
            self.ax2.set_title('GSR over Time')
            
            # Update canvas
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating plots: {e}")

    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.running = False

if __name__ == "__main__":
    monitor = SensorMonitor()
    monitor.run()
