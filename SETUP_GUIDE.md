# Guitar Tuner - Complete Step-by-Step Setup Guide

## Part 1: Preparing Your Raspberry Pi

### Step 1: Fresh Raspberry Pi Setup

1. **Install Raspberry Pi OS**
   ```bash
   # If starting fresh, download Raspberry Pi OS Lite or Desktop
   # Flash to SD card using Raspberry Pi Imager
   # Boot your Pi and complete initial setup
   ```

2. **Update System**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. **Enable Required Interfaces**
   ```bash
   # Run configuration tool
   sudo raspi-config
   
   # Navigate to:
   # - Interface Options → I2C → Enable (if using I2C LCD)
   # - Interface Options → SPI → Enable
   # - System Options → Audio → Select correct audio output
   
   # Reboot
   sudo reboot
   ```

---

## Part 2: Installing Dependencies

### Step 2: Install System Packages

```bash
# Install Python and development tools
sudo apt install -y python3 python3-pip python3-dev git

# Install audio libraries
sudo apt install -y portaudio19-dev python3-pyaudio

# Install GPIO libraries
sudo apt install -y python3-rpi.gpio

# Install build tools (for PyInstaller)
sudo apt install -y build-essential libffi-dev libssl-dev

# Optional: Install UPX for smaller executables
sudo apt install -y upx
```

### Step 3: Create Project Directory

```bash
# Create project folder
mkdir -p ~/guitar_tuner
cd ~/guitar_tuner
```

---

## Part 3: Copying Project Files

### Step 4: Transfer Files to Raspberry Pi

**Option A: Using SCP (from your computer)**
```bash
# From your computer, copy all files
scp -r /path/to/guitar_tuner/* pi@raspberrypi.local:~/guitar_tuner/
```

**Option B: Using USB Drive**
```bash
# On Pi, mount USB drive
sudo mkdir /mnt/usb
sudo mount /dev/sda1 /mnt/usb

# Copy files
cp -r /mnt/usb/guitar_tuner/* ~/guitar_tuner/

# Unmount
sudo umount /mnt/usb
```

**Option C: Using Git (if you have a repository)**
```bash
cd ~/guitar_tuner
git clone https://github.com/yourusername/guitar_tuner.git .
```

**Option D: Manual Creation**
```bash
# If you don't have files, create them manually
cd ~/guitar_tuner
nano config.py    # Copy content from the files I provided
nano hardware.py
nano audio.py
nano tuning.py
nano state.py
nano web_interface.py
nano main.py
nano build.py
nano requirements.txt
# etc.
```

### Step 5: Verify Files Are Present

```bash
cd ~/guitar_tuner
ls -la

# You should see:
# - main.py
# - config.py
# - hardware.py
# - audio.py
# - tuning.py
# - state.py
# - web_interface.py
# - build.py
# - test_modules.py
# - requirements.txt
# - Makefile
# - guitar_tuner.service
```

---

## Part 4: Installing Python Dependencies

### Step 6: Install Python Packages

```bash
cd ~/guitar_tuner

# Install all dependencies
pip3 install -r requirements.txt

# OR install manually:
pip3 install RPi.GPIO numpy pyaudio RPLCD Flask

# If you get permission errors, use:
pip3 install --user -r requirements.txt
```

### Step 7: Verify Installation

```bash
# Test that all modules can be imported
python3 test_modules.py

# Expected output:
#  Configuration (config.py)
#  Hardware Controller (hardware.py)
#  Audio Processor (audio.py)
#  Tuning Manager (tuning.py)
# Application State (state.py)
#  Web Interface (web_interface.py)
#  Main Application (main.py)
```

---

## Part 5: Hardware Configuration

### Step 8: Find Your Audio Device

```bash
# List audio input devices
arecord -l

# Output example:
# card 1: Device [USB Audio Device], device 0: USB Audio [USB Audio]

# Test your microphone
arecord -d 5 -f cd test.wav
aplay test.wav

# Find PyAudio device index
python3 << EOF
import pyaudio
pa = pyaudio.PyAudio()
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Index {i}: {info['name']}")
EOF

# Note the index number (usually 1 or 2)
```

### Step 9: Update Configuration

```bash
# Edit config.py with your audio device index
nano config.py

# Find this line:
# MIC_DEVICE_INDEX = 2

# Change the number to your device index from Step 8
# For example, if your device was index 1:
# MIC_DEVICE_INDEX = 1

# Save and exit (Ctrl+X, Y, Enter)
```

### Step 10: Verify GPIO Pins

```bash
# If using different pins, edit config.py
nano config.py

# Update these sections as needed:
# Button pins
BTN_LEFT = 4      # Change to your actual pin
BTN_RIGHT = 17    # Change to your actual pin
BTN_ENTER = 27    # Change to your actual pin
BTN_BACK = 22     # Change to your actual pin

# LED pins
LED_R = 5         # Change to your actual pin
LED_G = 6         # Change to your actual pin
LED_B = 13        # Change to your actual pin

# LCD pins
LCD_RS = 18       # Change to your actual pin
LCD_E = 23        # Change to your actual pin
LCD_DATA = [24, 25, 16, 20]  # Change to your actual pins
```

---

## Part 6: Testing Before Building

### Step 11: Test Run Without Building

```bash
cd ~/guitar_tuner

# Run directly (for testing)
python3 main.py

# You should see:
# Initializing Guitar Tuner...
# Web interface started on port 5000
# Guitar Tuner ready!

# Test the web interface
# Open browser to: http://raspberrypi.local:5000
# Or use IP: http://192.168.1.xxx:5000

# Press Ctrl+C to stop when done testing
```

### Step 12: Troubleshoot Issues

**If you get "No module named 'RPi.GPIO'":**
```bash
pip3 install RPi.GPIO --break-system-packages
```

**If you get "Permission denied" for GPIO:**
```bash
sudo usermod -a -G gpio $USER
# Log out and back in
```

**If LCD doesn't work:**
```bash
# Check connections
gpio readall

# For I2C LCD, check:
sudo i2cdetect -y 1
```

**If audio doesn't work:**
```bash
# Check audio devices
arecord -l
aplay -l

# Test microphone
arecord -d 5 test.wav
aplay test.wav
```

---

## Part 7: Building the Executable

### Step 13: Build Single Executable

```bash
cd ~/guitar_tuner

# Install PyInstaller
pip3 install pyinstaller

# Build executable
python3 build.py

# OR using Make:
make build

# Wait for build to complete (may take 5-10 minutes)
```

### Step 14: Verify Build

```bash
# Check that executable was created
ls -lh dist/guitar_tuner

# Should show file size (around 30-50 MB)

# Test the executable
./dist/guitar_tuner

# Should start the tuner
# Press Ctrl+C to stop
```

---

## Part 8: Final Installation

### Step 15: Install System-Wide (Optional)

```bash
# Copy executable to system location
sudo cp dist/guitar_tuner /usr/local/bin/

# Make it executable
sudo chmod +x /usr/local/bin/guitar_tuner

# Now you can run from anywhere
guitar_tuner
```

### Step 16: Set Up Auto-Start (Optional)

```bash
# Copy service file
sudo cp guitar_tuner.service /etc/systemd/system/

# Edit service file if needed (check paths)
sudo nano /etc/systemd/system/guitar_tuner.service

# Make sure paths are correct:
# WorkingDirectory=/home/pi/guitar_tuner
# ExecStart=/home/pi/guitar_tuner/dist/guitar_tuner

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable guitar_tuner.service
sudo systemctl start guitar_tuner.service

# Check status
sudo systemctl status guitar_tuner.service

# View logs
sudo journalctl -u guitar_tuner.service -f
```

---

## Part 9: Usage

### Step 17: Using Physical Buttons

1. **Power on** Raspberry Pi
2. **Wait** for boot (if auto-start enabled)
3. **Navigate** using buttons:
   - **LEFT/RIGHT**: Navigate menu options
   - **ENTER**: Select/Confirm
   - **BACK**: Go back to previous screen

4. **Select Guitar**: Choose 6 or 8 string
5. **Select Tuning**: Choose tuning preset
6. **Tune**: Play each string and watch:
   - **LCD**: Shows current note and cents offset
   - **LED**: 
     -  Green = In tune
     -  Yellow = Close
     -  Red = Far off

### Step 18: Using Web Interface

1. **Find Pi's IP Address**:
   ```bash
   hostname -I
   # Example output: 192.168.1.100
   ```

2. **Open Browser** on any device on same network

3. **Navigate** to: `http://192.168.1.100:5000`

4. **Use Interface**:
   - Select guitar type
   - Choose tuning
   - See real-time tuning data
   - Navigate strings with buttons

---

## Part 10: Maintenance

### Step 19: Updating Configuration

```bash
# Edit config
nano ~/guitar_tuner/config.py

# Rebuild
cd ~/guitar_tuner
python3 build.py

# Restart service (if using)
sudo systemctl restart guitar_tuner.service
```

### Step 20: Viewing Logs

```bash
# If running manually
python3 main.py

# If running as service
sudo journalctl -u guitar_tuner.service -f

# If running from cron
cat ~/guitar_tuner.log
```

---

## Quick Reference Card

### Common Commands

```bash
# Run directly
cd ~/guitar_tuner && python3 main.py

# Build executable
cd ~/guitar_tuner && python3 build.py

# Run executable
~/guitar_tuner/dist/guitar_tuner

# Start service
sudo systemctl start guitar_tuner.service

# Stop service
sudo systemctl stop guitar_tuner.service

# Check service status
sudo systemctl status guitar_tuner.service

# View logs
sudo journalctl -u guitar_tuner.service -f

# Find IP address
hostname -I
```

### File Locations

```
~/guitar_tuner/              - Project files
~/guitar_tuner/dist/         - Built executable
/usr/local/bin/guitar_tuner  - System-wide install
/etc/systemd/system/         - Service files
```

### Troubleshooting Commands

```bash
# Test audio
arecord -l
arecord -d 5 test.wav

# Test GPIO
gpio readall

# Test Python imports
python3 test_modules.py

# Check processes
ps aux | grep guitar_tuner

# Check network
netstat -tlnp | grep 5000
```

---

## Summary Checklist

- [ ] Raspberry Pi OS installed and updated
- [ ] System packages installed (Python, audio, GPIO)
- [ ] Project files copied to ~/guitar_tuner
- [ ] Python dependencies installed
- [ ] Audio device configured (MIC_DEVICE_INDEX)
- [ ] GPIO pins configured (if needed)
- [ ] Test run successful (python3 main.py)
- [ ] Executable built (python3 build.py)
- [ ] Web interface accessible (http://IP:5000)
- [ ] Auto-start configured (optional)

You're ready to tune!
