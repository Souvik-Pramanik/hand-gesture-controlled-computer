# 🖐️ Hand Gesture Controlled Computer

A Python-based computer-control system that uses a webcam and hand gestures to perform common computer actions.

The project uses **MediaPipe Hand Landmarker** for hand tracking, **OpenCV** for webcam processing, and Python automation libraries for controlling Windows functions.

---

## ✨ Features

* 🖐️ Real-time hand detection
* 👍 Volume Up
* 👎 Volume Down
* ✌️ Screenshot
* 👌 Play / Pause
* ✊ Windows Lock
* 🎥 Webcam-based interaction
* ⚡ Low-latency gesture response
* 🪟 Designed for Windows

---

## 🎮 Gesture Controls

| Gesture        | Action                 |
| -------------- | ---------------------- |
| 👍 Thumb Up    | Increase system volume |
| 👎 Thumb Down  | Decrease system volume |
| ✌️ Two Fingers | Take screenshot        |
| 👌 Pinch       | Play / Pause media     |
| ✊ Fist         | Lock Windows           |

> **Note:** Gesture recognition and response can vary slightly depending on lighting, camera quality, hand position, and detection conditions.

---

## 🧠 Technology Stack

* Python
* OpenCV
* MediaPipe
* NumPy
* PyAutoGUI
* Pycaw
* Comtypes

---

## 💻 System Requirements

### Hardware

* Windows PC
* Working webcam
* At least 4 GB RAM recommended

### Software

* Windows 10 or Windows 11
* Python 3.13+
* Git
* VS Code recommended

---

# 🚀 Installation

## 1. Clone the repository

Open PowerShell or the VS Code terminal:

```powershell
git clone https://github.com/Souvik-Pramanik/hand-gesture-controlled-computer.git
```

Enter the project directory:

```powershell
cd hand-gesture-controlled-computer
```

---

## 2. Create a Python virtual environment

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your terminal should show something similar to:

```text
(.venv) PS C:\Users\...\hand-gesture-controlled-computer>
```

---

## 3. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

## 4. Install project dependencies

```powershell
pip install -r requirements.txt
```

---

# 📦 Download the MediaPipe Model

The project uses the MediaPipe Hand Landmarker model.

Create the models directory:

```powershell
mkdir models
```

Download the model:

```powershell
Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -OutFile "models\hand_landmarker.task"
```

After downloading, your project should contain:

```text
models/
└── hand_landmarker.task
```

---

# 🔍 Verify the Installation

Check Python:

```powershell
python --version
```

Check MediaPipe:

```powershell
python -c "import mediapipe as mp; print(mp.__version__)"
```

Check OpenCV:

```powershell
python -c "import cv2; print(cv2.__version__)"
```

Check PyAutoGUI:

```powershell
python -c "import pyautogui; print('PyAutoGUI OK')"
```

Check Pycaw:

```powershell
python -c "from pycaw.pycaw import AudioUtilities; print('Pycaw OK')"
```

---

# ▶️ Run the Application

Make sure the virtual environment is activated:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then run:

```powershell
python main.py
```

A webcam window should open.

Place your hand in front of the camera and perform the supported gestures.

---

# 🖐️ How to Use

For best results:

1. Sit in a reasonably well-lit environment.
2. Keep your hand clearly visible to the webcam.
3. Avoid excessive background clutter.
4. Keep your hand within the camera frame.
5. Perform one gesture at a time.
6. Wait briefly between different gestures when necessary.

Press:

```text
Q
```

to exit the application.

---

# 📁 Project Structure

```text
hand-gesture-controlled-computer/
│
├── models/
│   └── hand_landmarker.task
│
├── main.py
├── gesture_recognition.py
├── actions.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .venv/
    └── (local virtual environment - not uploaded)
```

---

# 🔒 Privacy

The application processes webcam frames locally on your computer.

The project does not require uploading webcam footage to a remote server.

---

# ⚠️ Safety

The fist gesture can lock the Windows workstation.

Because this action affects the operating system, avoid accidental gestures while testing.

Do not use the application in situations where an unintended system action could cause harm or data loss.

---

# 🛠️ Troubleshooting

## Camera does not open

Try changing the camera index in `main.py`:

```python
cap = cv2.VideoCapture(0)
```

For another camera:

```python
cap = cv2.VideoCapture(1)
```

---

## MediaPipe model not found

Make sure this file exists:

```text
models\hand_landmarker.task
```

If it does not exist, download the model again using the installation command.

---

## PowerShell blocks virtual-environment activation

If PowerShell prevents activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Dependencies are missing

Run:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# 🔮 Future Improvements

* More reliable gesture classification
* Custom gesture training
* Mouse cursor control
* Scroll control
* Application launching
* Brightness control
* Keyboard shortcuts
* Multi-hand gestures
* Gesture customization
* GUI settings panel
* Improved gesture stability and calibration

---

# 👨‍💻 Development

Clone the repository:

```powershell
git clone https://github.com/Souvik-Pramanik/hand-gesture-controlled-computer.git
```

Create and activate the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python main.py
```

---

# 📜 License

This project is currently provided for educational and personal use.

A formal open-source license can be added later.

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
