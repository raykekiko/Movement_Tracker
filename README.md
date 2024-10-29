# Movement_Tracker
The Movement Tracker is a Python application that detects and logs movement across a designated line using optical flow. Built with OpenCV and Tkinter, this project includes a graphical interface for user interaction and real-time tracking.

Features
Real-Time Tracking: Captures live video feed, detecting motion across a middle line.
Event Logging: Logs entry and exit times when motion is detected crossing the line.
User-Friendly Interface: Uses Tkinter for a simple, interactive user experience.

Requirements
Python 3.x
OpenCV
NumPy
Tkinter (included in standard Python installations)
PIL (Pillow)


Code Overview
MovementTrackerApp Class: Initializes the UI, captures video, and tracks movement.
Optical Flow Calculation: Uses calcOpticalFlowFarneback to detect movement.
Logging: Records time-stamped events, visible in the main window.
