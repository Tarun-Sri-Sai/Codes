from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from datetime import datetime
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors


def clean_split(string: str, separator: str) -> list[str]:
    return [stripped_substring
            for substring in string.strip().split(separator)
            if (stripped_substring := substring.strip())]


def read_file(battery_stats_file):
    with open(battery_stats_file, 'r') as f:
        return [
            {
                'timestamp': int(words[0]),
                'battery_level': float(words[1])
            }
            for l in clean_split(f.read(), '\n')
            if len(words := clean_split(l, ' ')) > 1][-500:]


class BatteryLevelPlotter(tk.Tk):
    def __init__(self, file):
        super().__init__()
        self._file = file

        self.title("Battery Level Over Time")
        self.geometry("800x600")

        self.figure = plt.Figure(figsize=(10, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(
            side=tk.TOP, fill=tk.BOTH, expand=True)

        # Refresh button
        self.refresh_button = ttk.Button(
            self, text="Refresh", command=self.update_plot)
        self.refresh_button.pack(side=tk.BOTTOM, pady=10)

        self.schedule_update()

    def update_plot(self):
        self.ax.clear()
        times = []
        battery_levels = []

        data = sorted(read_file(self._file), key=lambda x: x['timestamp'])
        for entry in data:
            time_of_day = datetime.fromtimestamp(entry['timestamp'])
            times.append(time_of_day)
            battery_levels.append(entry['battery_level'])

        line, = self.ax.plot(times, battery_levels,
                             label='Battery Level', color='blue')
        self.ax.fill_between(times, battery_levels, color='skyblue', alpha=0.4)
        self.ax.set_xlabel('Time of Day (HH:MM)')
        self.ax.set_ylabel('Battery Level')
        self.ax.set_title('Battery Level Over Time')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

        # Set major locator
        locator = mdates.AutoDateLocator()
        self.ax.xaxis.set_major_locator(locator)

        self.figure.autofmt_xdate()
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

        # Add hover functionality
        cursor = mplcursors.cursor(line, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(
            f"Battery Level: {battery_levels[int(sel.index)]:.2f}\n"
            f"Time: {times[int(sel.index)]}"))

    def schedule_update(self):
        self.update_plot()
        # 300,000 milliseconds = 5 minutes
        self.after(300000, self.schedule_update)


def main():
    app = BatteryLevelPlotter('/var/log/battery-stats')
    app.mainloop()


if __name__ == '__main__':
    main()
