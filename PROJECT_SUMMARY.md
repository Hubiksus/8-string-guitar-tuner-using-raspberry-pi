# Guitar Tuner - Modular Refactoring Summary

## Overview


## File Structure

```
guitar_tuner/
│
├── Core Application Files
│   ├── main.py              (173 lines) - Application entry point and main loop
│   ├── config.py            ( 93 lines) - All constants and configuration
│   ├── hardware.py          (114 lines) - GPIO, LED, and LCD control
│   ├── audio.py             ( 79 lines) - Audio processing and pitch detection
│   ├── tuning.py            ( 72 lines) - Tuning data and logic
│   ├── state.py             ( 59 lines) - Application state management
│   └── web_interface.py     (389 lines) - Flask web server
│
├── Build & Deployment
│   ├── build.py             ( 65 lines) - Executable builder script
│   ├── test_modules.py      (106 lines) - Module import tester
│   ├── requirements.txt     (  5 lines) - Python dependencies
│   ├── Makefile             ( 28 lines) - Build automation
│   └── guitar_tuner.service ( 17 lines) - Systemd service file
│
└── Documentation
    ├── README.md            (160 lines) - Project documentation
    └── INSTALL.md           (258 lines) - Installation and deployment guide
```

## Key Improvements

### 1. Separation of Concerns
- **Hardware layer**: Isolated GPIO operations
- **Business logic**: Separate tuning calculations
- **State management**: Centralized app state
- **Web interface**: Independent web server
- **Configuration**: All constants in one place

### 2. Modularity Benefits
- **Easier testing**: Each module can be tested independently
- **Better maintenance**: Changes are localized to specific files
- **Code reuse**: Modules can be used in other projects
- **Cleaner imports**: Clear dependencies between modules

### 3. Build System
- **Single executable**: Build entire app into one file
- **Easy deployment**: Copy executable to any Raspberry Pi
- **Auto-start support**: Systemd service included
- **Make commands**: Simple build automation

## How to Use

### Quick Start (3 Steps)

```bash
# 1. Install dependencies
make install

# 2. Test everything works
make test

# 3. Build executable
make build
```

Your executable will be in: `dist/guitar_tuner`

### Running Options

**Option A: Development Mode**
```bash
python3 main.py
```

**Option B: Standalone Executable**
```bash
./dist/guitar_tuner
```

**Option C: Auto-start on Boot**
```bash
sudo cp guitar_tuner.service /etc/systemd/system/
sudo systemctl enable guitar_tuner.service
sudo systemctl start guitar_tuner.service
```

## Module Details

### config.py
- GPIO pin definitions (buttons, LEDs, LCD)
- Audio settings (sample rate, buffer size, device index)
- Tuning frequencies for all presets
- Web server configuration
- Threshold values for tuning accuracy

### hardware.py - HardwareController Class
**Methods:**
- `led_green/yellow/red/blue/off()` - LED control
- `is_button_pressed(pin)` - Check button state
- `wait_button_release(pin)` - Debounce handling
- `show_guitar_select()` - Display guitar selection screen
- `show_tuning_menu()` - Display tuning menu
- `show_tuner()` - Display tuning information
- `cleanup()` - Resource cleanup

### audio.py - AudioProcessor Class
**Methods:**
- `detect_pitch()` - Get current pitch from microphone
- `freq_to_cents(detected, target)` - Calculate tuning offset
- `cleanup()` - Close audio stream

### tuning.py - TuningManager Class (Static Methods)
**Methods:**
- `get_tunings_list(instrument)` - Get available tunings
- `get_string_order(tuning_name)` - Get strings sorted by frequency
- `find_closest_string(freq, tuning)` - Auto-detection logic
- `get_max_strings(instrument)` - String count

### state.py - AppState Class
**Properties:**
- `instrument` - Current instrument (6 or 8 strings)
- `selected_tuning_index` - Current tuning selection
- `current_string_index` - Current string being tuned
- `current_screen` - UI state machine
- `tuned_strings` - Tracking tuned strings
- `last_note`, `last_cents` - Detection results

**Methods:**
- `set_instrument(type)` - Switch instrument
- `change_screen(name)` - Navigate screens
- `navigate_tuning/string()` - Navigate options
- `mark_string_tuned()` - Track tuning progress
- `update_detection()` - Store detection results

### web_interface.py - WebInterface Class
**Routes:**
- `GET /` - Main page
- `POST /select_guitar` - Choose 6 or 8 string
- `POST /set_tuning` - Select tuning preset
- `POST /change_string` - Navigate strings
- `POST /back_to_guitar` - Return to selection
- `POST /back_to_tuning` - Return to tuning menu
- `GET /status` - JSON API for live updates

**Features:**
- Real-time tuning display
- Visual tuner needle
- String status grid
- Mobile-responsive design
- Auto-sync with hardware

### main.py - GuitarTuner Class
**Main Loop:**
1. Update LCD if state changed
2. Handle current screen (guitar/tuning/tuner)
3. Process audio in tuner mode
4. Update LED feedback
5. Repeat

**Screen Handlers:**
- `_handle_guitar_selection()` - 6 vs 8 string choice
- `_handle_tuning_menu()` - Tuning preset selection
- `_handle_tuner()` - Active tuning with audio processing

## Build Process

### What build.py Does

1. **Checks for PyInstaller** - Installs if missing
2. **Bundles all modules** - Packages Python files
3. **Includes dependencies** - Embeds numpy, Flask, etc.
4. **Creates executable** - Single file in dist/
5. **Adds hidden imports** - Ensures all imports work

### PyInstaller Options Used

```python
--onefile              # Single executable file
--name=guitar_tuner   # Output name
--hidden-import=...   # Include non-obvious imports
```

### Testing the Build

```bash
# Run test script
python3 test_modules.py

# Expected output:
 Configuration         (config.py)
 Hardware Controller   (hardware.py)
 Audio Processor      (audio.py)
 Tuning Manager       (tuning.py)
 Application State    (state.py)
 Web Interface        (web_interface.py)
 Main Application     (main.py)

 All modules imported successfully!
```

## Deployment Scenarios

### Scenario 1: Single Raspberry Pi
```bash
# Build once
python3 build.py

# Copy executable
sudo cp dist/guitar_tuner /usr/local/bin/

# Run from anywhere
guitar_tuner
```

### Scenario 2: Multiple Raspberry Pis
```bash
# Build on one Pi
python3 build.py

# Copy to others
scp dist/guitar_tuner pi@raspberrypi2:/home/pi/
scp dist/guitar_tuner pi@raspberrypi3:/home/pi/

# Run on each
ssh pi@raspberrypi2 "./guitar_tuner"
```

### Scenario 3: Production Deployment
```bash
# Install as service
sudo cp guitar_tuner.service /etc/systemd/system/
sudo systemctl enable guitar_tuner.service
sudo systemctl start guitar_tuner.service

# Monitor logs
sudo journalctl -u guitar_tuner.service -f
```

## Configuration Changes

To modify settings after building:

1. **Edit config.py** with your changes
2. **Rebuild**: `python3 build.py`
3. **Deploy new executable**

Common changes:
- Microphone device index
- GPIO pin numbers
- Web server port
- Tuning thresholds
- Add new tuning presets


## Extending the Application

### Adding a New Tuning

Edit `config.py`:
```python
TUNINGS_6_STRING.append("My Custom Tuning")

TUNING_FREQUENCIES["My Custom Tuning"] = {
    "E2": 82.41,
    "A2": 110.00,
    # ... add your frequencies
}
```

### Adding a New Feature

1. Decide which module it belongs to
2. Add the functionality to that module
3. Update `main.py` if needed to use it
4. Rebuild with `python3 build.py`

### Custom Hardware Layout

Edit `config.py` pin definitions:
```python
BTN_LEFT = 4    # Change to your pin
BTN_RIGHT = 17  # Change to your pin
# etc.
```

## Troubleshooting

See `INSTALL.md` for detailed troubleshooting including:
- Audio device configuration
- GPIO permissions
- Build errors
- Web interface issues
- LCD problems

## Files You Can Customize

- **config.py** - All settings and constants
- **build.py** - Build options and hidden imports
- **Makefile** - Build commands
- **guitar_tuner.service** - Service configuration

## Files You Shouldn't Need to Modify

- **main.py** - Main application logic (unless adding features)
- **hardware.py** - GPIO abstraction (unless changing hardware API)
- **audio.py** - Signal processing (unless changing algorithm)
- **tuning.py** - Tuning calculations (unless adding new logic)
- **state.py** - State management (unless changing state model)
- **web_interface.py** - Web server (unless changing UI)

## Next Steps

1. **Test the modules**: `python3 test_modules.py`
2. **Run in development**: `python3 main.py`
3. **Build executable**: `python3 build.py`
4. **Deploy**: Copy `dist/guitar_tuner` to your Pi
5. **Set up auto-start**: Use provided systemd service

## Support Files Included

- **README.md** - Project overview and usage
- **INSTALL.md** - Detailed installation guide
- **requirements.txt** - Python dependencies
- **Makefile** - Build automation
- **test_modules.py** - Import verification
- **guitar_tuner.service** - Systemd service
- **build.py** - Executable builder


Enjoy your guitar tuner!
