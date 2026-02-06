# Guitar Tuner - Installation & Deployment Guide

## Quick Start

### 1. Install Dependencies
```bash
make install
# or
pip3 install -r requirements.txt
```

### 2. Test Installation
```bash
make test
# or
python3 test_modules.py
```

### 3. Run the Application

**Option A: Run directly (for development)**
```bash
make run
# or
python3 main.py
```

**Option B: Build and run executable**
```bash
make build
# or
python3 build.py

# Then run
./dist/guitar_tuner
```

## Detailed Build Instructions

### Building the Executable

The build process uses PyInstaller to create a standalone executable:

```bash
# Install PyInstaller (done automatically by build.py)
pip3 install pyinstaller

# Build
python3 build.py

# Output will be in: dist/guitar_tuner
```

### Build Options

Edit `build.py` to customize:

```python
cmd = [
    "pyinstaller",
    "--onefile",              # Single file (can change to --onedir for folder)
    "--name=guitar_tuner",    # Change executable name
    "--console",              # Show console (add --noconsole to hide)
    # Add more options as needed
    "main.py"
]
```

### Testing the Build

```bash
# Test on the build machine
./dist/guitar_tuner

# Copy to another Raspberry Pi and test
scp dist/guitar_tuner pi@other-pi:/home/pi/
ssh pi@other-pi
./guitar_tuner
```

## Deployment Options

### Option 1: Manual Start

```bash
# Copy executable to desired location
sudo cp dist/guitar_tuner /usr/local/bin/

# Run manually
guitar_tuner
```

### Option 2: Auto-start on Boot (systemd)

```bash
# Copy service file
sudo cp guitar_tuner.service /etc/systemd/system/

# Edit paths in service file if needed
sudo nano /etc/systemd/system/guitar_tuner.service

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable guitar_tuner.service
sudo systemctl start guitar_tuner.service

# Check status
sudo systemctl status guitar_tuner.service

# View logs
sudo journalctl -u guitar_tuner.service -f
```

### Option 3: Cron Job (Start on Reboot)

```bash
# Edit crontab
crontab -e

# Add this line:
@reboot /home/pi/guitar_tuner/dist/guitar_tuner

# Or for logging:
@reboot /home/pi/guitar_tuner/dist/guitar_tuner >> /home/pi/guitar_tuner.log 2>&1
```

## Configuration

### Audio Device Configuration

If your microphone is on a different device index:

1. Find available audio devices:
```python
import pyaudio
pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    print(f"{i}: {info['name']}")
```

2. Update `config.py`:
```python
MIC_DEVICE_INDEX = 2  # Change to your device index
```

3. Rebuild the executable:
```bash
python3 build.py
```

### GPIO Pin Configuration

To change GPIO pins, edit `config.py`:

```python
# Button pins
BTN_LEFT = 4
BTN_RIGHT = 17
BTN_ENTER = 27
BTN_BACK = 22

# LED pins
LED_R = 5
LED_G = 6
LED_B = 13

# LCD pins
LCD_RS = 18
LCD_E = 23
LCD_DATA = [24, 25, 16, 20]
```

### Web Server Configuration

Edit `config.py`:

```python
WEB_HOST = "0.0.0.0"  # Listen on all interfaces
WEB_PORT = 5000       # Change port if needed
```

## Troubleshooting

### Import Errors

If you get import errors when running the executable:

1. Add missing imports to `build.py`:
```python
"--hidden-import=missing_module",
```

2. Rebuild:
```bash
python3 build.py
```

### GPIO Permission Errors

```bash
# Add user to gpio group
sudo usermod -a -G gpio $USER

# Or run with sudo (not recommended for production)
sudo ./dist/guitar_tuner
```

### Audio Device Not Found

```bash
# List audio devices
arecord -l

# Test recording
arecord -d 5 test.wav

# Check PyAudio devices
python3 -c "import pyaudio; pa = pyaudio.PyAudio(); [print(i, pa.get_device_info_by_index(i)) for i in range(pa.get_device_count())]"
```

### Web Interface Not Accessible

```bash
# Check if port is open
sudo netstat -tlnp | grep 5000

# Check firewall
sudo ufw status

# Allow port if needed
sudo ufw allow 5000

# Find Raspberry Pi IP
hostname -I
```

### LCD Not Working

```bash
# Test I2C devices (if using I2C LCD)
sudo i2cdetect -y 1

# Check GPIO connections
gpio readall
```

## Performance Optimization

### For Faster Startup

Build with compiled Python files:

```bash
# Compile Python files
python3 -m compileall .

# Build with optimizations
pyinstaller --onefile --optimize=2 main.py
```

### For Smaller Executable

```bash
# Use UPX compression (install first)
sudo apt-get install upx

# Build with compression
pyinstaller --onefile --upx-dir=/usr/bin main.py
```

## Distribution

### Creating a Release Package

```bash
# Create release directory
mkdir guitar_tuner_release
cd guitar_tuner_release

# Copy files
cp ../dist/guitar_tuner .
cp ../README.md .
cp ../guitar_tuner.service .

# Create archive
tar -czf guitar_tuner_v1.0.tar.gz *

# Or create zip
zip -r guitar_tuner_v1.0.zip *
```

### Installation on Target System

```bash
# Extract
tar -xzf guitar_tuner_v1.0.tar.gz

# Make executable
chmod +x guitar_tuner

# Run
./guitar_tuner
```

## Backup Configuration

```bash
# Backup current settings
cp config.py config.py.backup

# Restore settings
cp config.py.backup config.py
```

## Updating

```bash
# Pull latest changes
git pull

# Reinstall dependencies
make install

# Test
make test

# Rebuild
make build

# Restart service
sudo systemctl restart guitar_tuner.service
```
