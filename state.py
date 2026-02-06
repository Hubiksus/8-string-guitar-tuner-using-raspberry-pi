"""
Application state module
Manages the current state of the tuner application
"""


class AppState:
    """Centralized application state manager"""
    
    def __init__(self):
        # Instrument configuration
        self.instrument = None  # "6" or "8"
        self.selected_tuning_index = 0
        
        # Tuning state
        self.current_string_index = 0
        self.tuned_strings = {}  # Dict of strings that have been tuned
        
        # UI state
        self.current_screen = "select_guitar"  # select_guitar, tuning_menu, tuner
        self.update_lcd = True  # Flag to trigger LCD refresh
        
        # Last detected values (for display)
        self.last_note = "---"
        self.last_cents = "---"
        self.last_cents_raw = 0
    
    def reset_tuning_state(self):
        """Reset tuning-related state"""
        self.current_string_index = 0
        self.tuned_strings = {}
        self.last_note = "---"
        self.last_cents = "---"
        self.last_cents_raw = 0
    
    def set_instrument(self, instrument):
        """Set the instrument type"""
        self.instrument = instrument
        self.selected_tuning_index = 0
        self.reset_tuning_state()
    
    def change_screen(self, screen_name):
        """Change the current screen"""
        self.current_screen = screen_name
        self.update_lcd = True
    
    def navigate_tuning(self, direction, max_tunings):
        """Navigate through tuning options"""
        self.selected_tuning_index = (self.selected_tuning_index + direction) % max_tunings
        self.update_lcd = True
    
    def navigate_string(self, direction, max_strings):
        """Navigate through strings"""
        self.current_string_index = (self.current_string_index + direction) % max_strings
        self.update_lcd = True
    
    def set_string_index(self, index):
        """Set the current string index"""
        if index != self.current_string_index:
            self.current_string_index = index
            self.update_lcd = True
    
    def mark_string_tuned(self, note_name):
        """Mark a string as tuned"""
        self.tuned_strings[note_name] = True
    
    def update_detection(self, note, cents_value):
        """Update detected note and cents"""
        self.last_note = note
        self.last_cents = f"{cents_value:+.1f}" if cents_value is not None else "---"
        self.last_cents_raw = cents_value if cents_value is not None else 0
