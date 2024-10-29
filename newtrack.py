import cv2
import numpy as np
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MovementTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Movement Tracker")
        self.master.geometry("800x600")
        self.master.configure(bg="#6e45e1")

        # Title
        self.title_label = tk.Label(master, text="Welcome to the Movement Tracker", font=("Arial", 18, "bold"), bg="#6e45e1", fg="#fff")
        self.title_label.pack(pady=20)

        # Name input
        self.name_label = tk.Label(master, text="Enter your name:", font=("Arial", 12), bg="#6e45e1", fg="#fff")
        self.name_label.pack()

        self.name_entry = tk.Entry(master, font=("Arial", 12), width=30)
        self.name_entry.pack(pady=10)

        # Start button
        self.start_button = tk.Button(master, text="Start Tracking", command=self.start_tracking, font=("Arial", 14, "bold"), bg="#6200ea", fg="#fff", activebackground="#3700b3")
        self.start_button.pack(pady=10)

        # Status output
        self.status_label = tk.Label(master, text="", font=("Arial", 12), bg="#6e45e1", fg="#fff")
        self.status_label.pack(pady=20)

        # Log display
        self.log_label = tk.Label(master, text="Event Log:", font=("Arial", 12, "bold"), bg="#6e45e1", fg="#fff")
        self.log_label.pack(pady=10)
        
        self.log_text = tk.Text(master, width=50, height=10, font=("Arial", 10))
        self.log_text.pack(pady=5)

        # Initialize variables
        self.cap = None
        self.tracking = False
        self.prev_position = None
        self.log = []
        self.mid_line_x = None  # Middle line x-coordinate

    def start_tracking(self):
        name = self.name_entry.get().strip()
        if name:
            self.status_label.config(text=f"Tracking {name}...")
            self.tracking = True
            self.track_movement(name)
        else:
            messagebox.showwarning("Input Error", "Please enter your name!")

    def track_movement(self, name):
        # Open a new window for the live feed
        self.tracking_window = tk.Toplevel(self.master)
        self.tracking_window.title(f"{name}'s Movement Tracking")
        self.tracking_window.geometry("800x600")
        self.tracking_window.configure(bg="#1e1e1e")

        self.video_label = tk.Label(self.tracking_window)
        self.video_label.pack(pady=20)

        # Capture video
        self.cap = cv2.VideoCapture(0)
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="Failed to access the camera.")
            return

        # Set the middle line x-coordinate
        self.mid_line_x = frame.shape[1] // 2

        # Initialize initial frame for optical flow
        prev_gray = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2GRAY)

        while self.tracking:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Pre-process the frame
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Draw the middle line
            cv2.line(frame, (self.mid_line_x, 0), (self.mid_line_x, frame.shape[0]), (0, 255, 0), 2)

            # Calculate dense optical flow
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

            # Average flow direction and position
            avg_flow_x = np.mean(flow[..., 0])
            avg_position = np.mean(np.where(magnitude > 2)[1])  # Average x-position of significant flow

            # Determine entry/exit and log the event
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            if avg_flow_x > 2 and avg_position > self.mid_line_x and (self.prev_position is None or self.prev_position <= self.mid_line_x):
                self.log_event(f"{name} has gone out at {current_time}.")
                self.prev_position = avg_position
            elif avg_flow_x < -2 and avg_position < self.mid_line_x and (self.prev_position is None or self.prev_position >= self.mid_line_x):
                self.log_event(f"{name} has come in at {current_time}.")
                self.prev_position = avg_position

            # Display the frame
            self.display_frame(frame)

            # Update the previous frame
            prev_gray = gray.copy()

            self.tracking_window.update()
            if cv2.waitKey(1) & 0xFF == 27:  # Stop on 'ESC' key
                self.tracking = False
                break

        self.cap.release()
        self.tracking_window.destroy()

    def log_event(self, message):
        """Log the event with a timestamp and display it in the log window."""
        self.log.append(message)
        self.status_label.config(text=message)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Auto-scroll to the latest log

    def display_frame(self, frame):
        """Display the frame in the Tkinter label."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        img_pil = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = MovementTrackerApp(root)
    root.mainloop()
