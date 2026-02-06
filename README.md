# Guitar Tuner - Modular Version

This is the refactored, modular version of the Guitar Tuner application.

## Project Structure

```
guitar_tuner/
├── main.py              # Main application entry point
├── config.py            # Configuration and constants
├── hardware.py          # GPIO, LED, and LCD control
├── audio.py             # Audio processing and pitch detection
├── tuning.py            # Tuning data and logic
├── state.py             # Application state management
├── web_interface.py     # Flask web server
├── requirements.txt     # Python dependencies
├── build.py             # Script to build executable
└── README.md            # This file
```

## Module Descriptions

### config.py
Contains all configuration constants including:
- GPIO pin definitions
- Audio settings
- Tuning data and frequencies
- Web server configuration

### hardware.py
Handles all hardware interactions:
- Button input reading
- RGB LED control
- LCD display management
- GPIO cleanup

### audio.py
Audio processing module:
- Microphone input capture
- Pitch detection using autocorrelation
- Frequency to cents conversion

### tuning.py
Tuning logic:
- Tuning data retrieval
- String ordering
- Closest string detection (for auto mode)

### state.py
Application state management:
- Current screen tracking
- String and tuning selection
- Tuned strings tracking
- Last detected values

### web_interface.py
Flask web interface:
- Web routes and endpoints
- HTML template
- JSON API for live updates
- Background server thread

### main.py
Main application controller:
- Initializes all modules
- Main event loop
- Screen handling logic
- Ties everything together

## Running the Application

### Option 1: Run Directly
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py
```

### Option 2: Build and Run Executable
```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
python3 build.py

# Run the executable
./dist/guitar_tuner
```

## Building the Executable

The `build.py` script uses PyInstaller to create a single executable file:

1. Installs PyInstaller if not present
2. Bundles all Python modules
3. Includes all dependencies
4. Creates a standalone executable in `dist/guitar_tuner`

### Build Options

You can customize the build by modifying `build.py`:
- Change executable name with `--name`
- Add more hidden imports if needed
- Include additional data files with `--add-data`

### Manual Build

If you prefer to build manually:

```bash
pyinstaller --onefile \
  --name=guitar_tuner \
  --hidden-import=RPi.GPIO \
  --hidden-import=numpy \
  --hidden-import=pyaudio \
  --hidden-import=RPLCD \
  --hidden-import=flask \
  main.py
```

## Usage

1. **Physical Interface**: Use the hardware buttons on the Raspberry Pi
   - LEFT/RIGHT: Navigate options
   - ENTER: Select/confirm
   - BACK: Go back to previous screen

2. **Web Interface**: Access from any device on the network
   - Open browser to `http://<raspberry-pi-ip>:5000`
   - Full remote control and monitoring

## Features

- **6 and 8 string guitar support**
- **Multiple tuning presets** (E Standard, Drop D, Drop C, etc.)
- **Real-time pitch detection** using autocorrelation
- **Visual feedback** with RGB LED (green=tuned, yellow=close, red=far)
- **LCD display** showing current string and tuning offset
- **Web interface** for remote monitoring and control
- **Auto-detection mode** for 6-string E Standard tuning

## Hardware Requirements

- Raspberry Pi (any model with GPIO)
- 16x2 LCD display
- 4 push buttons (Left, Right, Enter, Back)
- RGB LED
- USB sound card/microphone
- Appropriate resistors and wiring

## Troubleshooting

### Audio Device Issues
If the microphone is not found, check available devices:
```python
import pyaudio
pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    print(i, pa.get_device_info_by_index(i)['name'])
```

Update `MIC_DEVICE_INDEX` in `config.py` with the correct index.

### GPIO Permissions
If you get GPIO permission errors, run with sudo or add user to gpio group:
```bash
sudo usermod -a -G gpio $USER
```

### Build Issues
If PyInstaller build fails:
1. Ensure all dependencies are installed
2. Try building without `--onefile` first
3. Check PyInstaller logs in `build/` directory

## License

This project is provided as-is for educational and personal use.
