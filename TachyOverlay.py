import pip._vendor.requests as requests
import tkinter as tk

class TachyOverlay:
    def __init__(self, master):
        self.master = master
        self.master.title("TachyOverlay")
        self.master.configure(bg="black")

        self.labels = []

        volumeLabel = tk.Label(master, text="Volume: 0", font=("Helvetica", 16),
            bg="black", fg="white", anchor="w", justify="left")
        mouseSensLabel = tk.Label(master, text="Sens: 10", font=("Helvetica", 16),
            bg="black", fg="white", anchor="w", justify="left")
        keyHoldLabel = tk.Label(master, text="Key Held: NULL", font=("Helvetica", 16),
            bg="black", fg="white", anchor="w", justify="left")

        volumeLabel.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        mouseSensLabel.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        keyHoldLabel.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.labels.extend([volumeLabel, mouseSensLabel, keyHoldLabel])

        self.update_loop()

    @staticmethod
    def rangeAdjust(oldMin, oldMax, newMin, newMax, val):
        oldRange = oldMax - oldMin
        newRange = newMax - newMin
        if oldRange == 0:
            return newMin
        newValue = (((val - oldMin) * newRange) / oldRange) + newMin

        return max(min(newValue, newMax), newMin)

    def fetch_and_update(self):
        try:
            # ---------------------------------------SETTINGS----------------------------------

            minHR, maxHR = 80, 200 # set mins and maxes for HR
            minVol, maxVol = 10, 100 # set mins and maxes for volume (0-100)
            minSens, maxSens = 1, 20 # set mins and maxes for mouse sense (1-20)
            keyHeld = "Shift"

            # -----------------------------------------API-------------------------------------

            APIKEY = ""
            url = "https://dev.pulsoid.net/api/v1/data/heart_rate/latest?response_mode=text_plain_only_heart_rate"
            headers = {
                "Authorization": "Bearer " + APIKEY,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            heartrate = int(response.text)
            print(heartrate)

            # ---------------------------------------FUNCTION----------------------------------

            volume = round(self.rangeAdjust(minHR, maxHR, minVol, maxVol, heartrate))
            mouseSens = round(self.rangeAdjust(minHR, maxHR, minSens, maxSens, heartrate))

            self.master.after(0, lambda: self.labels[0].config(text=f"Volume: {volume}"))
            self.master.after(0, lambda: self.labels[1].config(text=f"Sens: {mouseSens}"))

            if heartrate < minHR:
                self.master.after(0, lambda: self.labels[2].config(text=f"Key Held: {keyHeld}", fg="red"))
            else:
                self.master.after(0, lambda: self.labels[2].config(text="Key Held: None", fg="white"))

        except Exception as e:
            self.master.after(0, lambda: self.labels[2].config(text="Error fetching HR", fg="red"))
            print(f"Error: {e}")

    def update_loop(self):
        self.fetch_and_update()
        self.master.after(1000, self.update_loop)  # Call again every second

if __name__ == "__main__":
    root = tk.Tk()
    app = TachyOverlay(root)
    root.mainloop()
