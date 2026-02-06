"""
Hardware module for GPIO control
Handles buttons, RGB LED, and LCD display
"""

import RPi.GPIO as GPIO
import time
from RPLCD import CharLCD
from config import (
    BTN_LEFT, BTN_RIGHT, BTN_ENTER, BTN_BACK,
    LED_R, LED_G, LED_B,
    LCD_RS, LCD_E, LCD_DATA
)


class HardwareController:
    """Manages all GPIO hardware interactions"""
    
    def __init__(self):
        # Set pin numbering mode to BCM
        GPIO.setmode(GPIO.BCM)
        
        # Initialize buttons
        self.buttons = [BTN_LEFT, BTN_RIGHT, BTN_ENTER, BTN_BACK]
        for pin in self.buttons:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Initialize RGB LED
        GPIO.setup([LED_R, LED_G, LED_B], GPIO.OUT)
        self.led_off()
        
        # Initialize LCD
        self.lcd = CharLCD(
            numbering_mode=GPIO.BCM, 
            cols=16, 
            rows=2,
            pin_rs=LCD_RS, 
            pin_rw=None, 
            pin_e=LCD_E, 
            pins_data=LCD_DATA
        )
    
    # ============================================================
    # LED CONTROL METHODS
    # ============================================================
    def led_off(self):
        """Turn off all LED colors"""
        GPIO.output([LED_R, LED_G, LED_B], [0, 0, 0])
    
    def led_green(self):
        """Set LED to green (in-tune signal)"""
        GPIO.output([LED_R, LED_G, LED_B], [0, 1, 0])
    
    def led_yellow(self):
        """Set LED to yellow (slightly out of tune)"""
        GPIO.output([LED_R, LED_G, LED_B], [1, 1, 0])
    
    def led_red(self):
        """Set LED to red (significantly out of tune)"""
        GPIO.output([LED_R, LED_G, LED_B], [1, 0, 0])
    
    def led_blue(self):
        """Set LED to blue (system/processing state)"""
        GPIO.output([LED_R, LED_G, LED_B], [0, 0, 1])
    
    # ============================================================
    # BUTTON METHODS
    # ============================================================
    def is_button_pressed(self, button_pin):
        """Check if a button is currently pressed"""
        return GPIO.input(button_pin) == 0
    
    def wait_button_release(self, button_pin):
        """Wait for a button to be released"""
        while GPIO.input(button_pin) == 0:
            time.sleep(0.01)
        time.sleep(0.1)
    
    # ============================================================
    # LCD DISPLAY METHODS
    # ============================================================
    def clear_display(self):
        """Clear the LCD display"""
        self.lcd.clear()
    
    def write_text(self, text, row=0, col=0):
        """Write text to LCD at specified position"""
        self.lcd.cursor_pos = (row, col)
        self.lcd.write_string(text)
    
    def show_guitar_select(self):
        """Render the instrument selection screen"""
        self.lcd.clear()
        self.lcd.write_string("Choose Guitar:")
    
    def show_tuning_menu(self, instrument, tuning_name):
        """Render the tuning selection screen"""
        self.lcd.clear()
        self.lcd.write_string(f"Tuning ({instrument}-str):")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"{tuning_name}".ljust(16))
    
    def show_tuner(self, note="---", cents="---", string_num=None, max_str=None):
        """Render the real-time tuning screen"""
        self.lcd.clear()
        str_info = f"{note} ({string_num}/{max_str})" if note and string_num else "---"
        self.lcd.write_string(f"Str:{str_info}")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"Cents:{cents}" if cents else "---")
    
    # ============================================================
    # CLEANUP
    # ============================================================
    def cleanup(self):
        """Clean up GPIO resources"""
        self.led_off()
        GPIO.cleanup()
