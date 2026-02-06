"""
Configuration file for Guitar Tuner
Contains all constants, GPIO pin definitions, and tuning data
"""

# ============================================================
# GPIO PIN DEFINITIONS
# ============================================================
# Push button pins
BTN_LEFT = 4
BTN_RIGHT = 17
BTN_ENTER = 27
BTN_BACK = 22

# RGB LED pins
LED_R = 5
LED_G = 6
LED_B = 13

# LCD pins
LCD_RS = 18
LCD_E = 23
LCD_DATA = [24, 25, 16, 20]

# ============================================================
# AUDIO CONFIGURATION
# ============================================================
NUM_SAMPLES = 4096
SAMPLING_RATE = 48000
MIC_DEVICE_INDEX = 2

# ============================================================
# TUNING THRESHOLDS (in cents)
# ============================================================
THRESHOLD_PERFECT = 15  # Green LED - in tune
THRESHOLD_CLOSE = 30    # Yellow LED - close to tune

# ============================================================
# TUNINGS DATA
# ============================================================
TUNINGS_6_STRING = [
    "E Standard", "Drop D", "D Standard", "Drop C", 
    "Drop C#", "Drop B", "Drop A", "Drop A#", "Drop G"
]

TUNINGS_8_STRING = [
    "Standard F#", "Drop E", "Drop D", 
    "E Standard", "F Standard", "Double Drop D"
]

# Frequency map for specific notes in Hertz (Hz)
TUNING_FREQUENCIES = {
    "E Standard": {
        "E2": 82.41, "A2": 110, "D3": 146.83, 
        "G3": 196, "B3": 246.94, "E4": 329.63
    },
    "Drop D": {
        "D2": 73.42, "A2": 110, "D3": 146.83, 
        "G3": 196, "B3": 246.94, "E4": 329.63
    },
    "D Standard": {
        "D2": 73.42, "G2": 98, "C3": 130.81, 
        "F3": 174.61, "A3": 220, "D4": 293.66
    },
    "Drop C": {
        "C2": 65.41, "G2": 98, "C3": 130.81, 
        "F3": 174.61, "A3": 220, "D4": 293.66
    },
    "Drop C#": {
        "C#2": 69.3, "G#2": 103.83, "C#3": 138.59, 
        "F#3": 185, "A3": 220, "D4": 293.66
    },
    "Drop B": {
        "B1": 61.74, "F#2": 92.5, "B2": 123.47, 
        "E3": 164.81, "G#3": 207.65, "C#4": 277.18
    },
    "Drop A": {
        "A1": 55, "E2": 82.41, "A2": 110, 
        "D3": 146.83, "F#3": 185, "B3": 246.94
    },
    "Drop A#": {
        "A#1": 58.27, "F2": 87.31, "A#2": 116.54, 
        "D3": 146.83, "F3": 174.61, "A3": 220
    },
    "Drop G": {
        "G1": 49, "D2": 73.42, "G2": 98, 
        "C3": 130.81, "E3": 164.81, "G3": 196
    },
    "Standard F#": {
        "F#1": 46.25, "B1": 61.74, "E2": 82.41, "A2": 110, 
        "D3": 146.83, "G3": 196, "B3": 246.94, "E4": 329.63
    },
    "Drop E": {
        "E1": 41.2, "B1": 61.74, "E2": 82.41, "A2": 110, 
        "D3": 146.83, "G3": 196, "B3": 246.94, "E4": 329.63
    },
    "F Standard": {
        "F1": 43.65, "A1": 55, "D2": 73.42, "G2": 98, 
        "B2": 123.47, "E3": 164.81, "A3": 220
    },
    "Double Drop D": {
        "D1": 36.71, "A1": 55, "D2": 73.42, "G2": 98, 
        "B2": 123.47, "E3": 164.81, "A3": 220, "D4": 293.66
    },
}

# ============================================================
# WEB SERVER CONFIGURATION
# ============================================================
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
