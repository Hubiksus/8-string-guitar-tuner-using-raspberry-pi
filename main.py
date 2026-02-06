#!/usr/bin/env python3
"""
Guitar Tuner Main Application
Ties together all modules and runs the main control loop
"""

import time
from hardware import HardwareController
from audio import AudioProcessor
from tuning import TuningManager
from state import AppState
from web_interface import WebInterface
from config import (
    BTN_LEFT, BTN_RIGHT, BTN_ENTER, BTN_BACK,
    THRESHOLD_PERFECT, THRESHOLD_CLOSE
)


class GuitarTuner:
    """Main application controller"""
    
    def __init__(self):
        print("Initializing Guitar Tuner...")
        
        # Initialize all components
        self.hardware = HardwareController()
        self.audio = AudioProcessor()
        self.state = AppState()
        self.web = WebInterface(self.state)
        
        # Start web server
        self.web.start()
        print("Web interface started on port 5000")
        
        # Local navigation state for guitar selection
        self.guitar_options = ["6", "8"]
        self.guitar_index = 0
    
    def run(self):
        """Main application loop"""
        try:
            print("Guitar Tuner ready!")
            
            while True:
                # Update LCD if needed
                if self.state.update_lcd:
                    self._update_display()
                    self.state.update_lcd = False
                
                # Handle current screen
                if self.state.current_screen == "select_guitar":
                    self._handle_guitar_selection()
                
                elif self.state.current_screen == "tuning_menu":
                    self._handle_tuning_menu()
                
                elif self.state.current_screen == "tuner":
                    self._handle_tuner()
                
                # Small sleep to prevent CPU hogging
                time.sleep(0.01)
        
        except KeyboardInterrupt:
            print("\nShutting down...")
        
        finally:
            self.cleanup()
    
    def _update_display(self):
        """Update LCD based on current screen"""
        if self.state.current_screen == "select_guitar":
            self.hardware.show_guitar_select()
        
        elif self.state.current_screen == "tuning_menu":
            tunings_list = TuningManager.get_tunings_list(self.state.instrument)
            tuning_name = tunings_list[self.state.selected_tuning_index]
            self.hardware.show_tuning_menu(self.state.instrument, tuning_name)
        
        elif self.state.current_screen == "tuner":
            max_str = TuningManager.get_max_strings(self.state.instrument)
            self.hardware.show_tuner(
                note=self.state.last_note,
                cents=self.state.last_cents,
                string_num=self.state.current_string_index + 1,
                max_str=max_str
            )
    
    def _handle_guitar_selection(self):
        """Handle guitar selection screen logic"""
        # Update display with current selection
        self.hardware.write_text(f"{self.guitar_options[self.guitar_index]}-String".ljust(16), row=1, col=0)
        
        # Handle button presses
        if self.hardware.is_button_pressed(BTN_LEFT):
            self.guitar_index = (self.guitar_index - 1) % len(self.guitar_options)
            self.hardware.wait_button_release(BTN_LEFT)
        
        if self.hardware.is_button_pressed(BTN_RIGHT):
            self.guitar_index = (self.guitar_index + 1) % len(self.guitar_options)
            self.hardware.wait_button_release(BTN_RIGHT)
        
        if self.hardware.is_button_pressed(BTN_ENTER):
            self.state.set_instrument(self.guitar_options[self.guitar_index])
            self.state.change_screen("tuning_menu")
            self.hardware.wait_button_release(BTN_ENTER)
    
    def _handle_tuning_menu(self):
        """Handle tuning menu screen logic"""
        tunings_list = TuningManager.get_tunings_list(self.state.instrument)
        
        # Handle button presses
        if self.hardware.is_button_pressed(BTN_LEFT):
            self.state.navigate_tuning(-1, len(tunings_list))
            self.hardware.wait_button_release(BTN_LEFT)
        
        if self.hardware.is_button_pressed(BTN_RIGHT):
            self.state.navigate_tuning(1, len(tunings_list))
            self.hardware.wait_button_release(BTN_RIGHT)
        
        if self.hardware.is_button_pressed(BTN_ENTER):
            self.state.reset_tuning_state()
            self.state.change_screen("tuner")
            self.hardware.wait_button_release(BTN_ENTER)
        
        if self.hardware.is_button_pressed(BTN_BACK):
            self.state.instrument = None
            self.state.reset_tuning_state()
            self.state.change_screen("select_guitar")
            self.hardware.wait_button_release(BTN_BACK)
    
    def _handle_tuner(self):
        """Handle tuner screen logic"""
        max_str = TuningManager.get_max_strings(self.state.instrument)
        tunings_list = TuningManager.get_tunings_list(self.state.instrument)
        tuning_name = tunings_list[self.state.selected_tuning_index]
        
        # Check for special auto-detection mode (6-string E Standard)
        auto_detect = (self.state.instrument == "6" and tuning_name == "E Standard")
        
        # Handle navigation (disabled in auto mode)
        if self.hardware.is_button_pressed(BTN_LEFT):
            if not auto_detect:
                self.state.navigate_string(-1, max_str)
            self.hardware.wait_button_release(BTN_LEFT)
        
        if self.hardware.is_button_pressed(BTN_RIGHT):
            if not auto_detect:
                self.state.navigate_string(1, max_str)
            self.hardware.wait_button_release(BTN_RIGHT)
        
        if self.hardware.is_button_pressed(BTN_BACK):
            self.state.change_screen("tuning_menu")
            self.hardware.wait_button_release(BTN_BACK)
        
        # Audio processing
        freq = self.audio.detect_pitch()
        
        if auto_detect:
            # Auto-detect closest string
            idx, note, target_freq, cents = TuningManager.find_closest_string(freq, tuning_name)
            if idx is not None:
                self.state.set_string_index(idx)
        else:
            # Manual string selection
            order = TuningManager.get_string_order(tuning_name)
            if self.state.current_string_index < len(order):
                note, target_freq = order[self.state.current_string_index]
                cents = AudioProcessor.freq_to_cents(freq, target_freq)
            else:
                note, target_freq, cents = None, None, None
        
        # Update LED feedback
        if cents is not None:
            abs_cents = abs(cents)
            if abs_cents <= THRESHOLD_PERFECT:
                self.hardware.led_green()
                if note:
                    self.state.mark_string_tuned(note)
            elif abs_cents <= THRESHOLD_CLOSE:
                self.hardware.led_yellow()
            else:
                self.hardware.led_red()
        else:
            self.hardware.led_off()
        
        # Update state
        self.state.update_detection(note, cents)
        
        # Update display
        self.hardware.show_tuner(
            note=self.state.last_note,
            cents=self.state.last_cents,
            string_num=self.state.current_string_index + 1,
            max_str=max_str
        )
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        self.hardware.cleanup()
        self.audio.cleanup()
        print("Goodbye!")


def main():
    """Entry point for the application"""
    tuner = GuitarTuner()
    tuner.run()


if __name__ == "__main__":
    main()
