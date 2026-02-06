"""
Tuning logic module
Handles tuning data and string order management
"""

from config import TUNING_FREQUENCIES, TUNINGS_6_STRING, TUNINGS_8_STRING


class TuningManager:
    """Manages tuning configurations and string data"""
    
    @staticmethod
    def get_tunings_list(instrument):
        """
        Get list of available tunings for an instrument
        
        Args:
            instrument: "6" or "8" for string count
        
        Returns:
            List of tuning names
        """
        if instrument == "6":
            return TUNINGS_6_STRING
        elif instrument == "8":
            return TUNINGS_8_STRING
        return []
    
    @staticmethod
    def get_string_order(tuning_name):
        """
        Get strings and their frequencies sorted from lowest to highest
        
        Args:
            tuning_name: Name of the tuning
        
        Returns:
            List of (note_name, frequency) tuples sorted by frequency
        """
        if tuning_name not in TUNING_FREQUENCIES:
            return []
        
        tuning = TUNING_FREQUENCIES[tuning_name]
        return sorted(tuning.items(), key=lambda x: x[1])
    
    @staticmethod
    def find_closest_string(detected_freq, tuning_name):
        """
        Find the closest string to a detected frequency
        Used for auto-detection mode
        
        Args:
            detected_freq: Detected frequency in Hz
            tuning_name: Current tuning name
        
        Returns:
            Tuple of (string_index, note_name, target_freq, cents_offset)
        """
        if tuning_name not in TUNING_FREQUENCIES:
            return None, None, None, None
        
        from audio import AudioProcessor
        
        min_diff = 1e6
        closest_string = None
        closest_index = None
        target_freq = None
        
        tuning = TUNING_FREQUENCIES[tuning_name]
        string_order = sorted(tuning.items(), key=lambda x: x[1])
        
        for idx, (note, freq) in enumerate(string_order):
            cents = AudioProcessor.freq_to_cents(detected_freq, freq)
            if cents is not None and abs(cents) < abs(min_diff):
                min_diff = cents
                closest_string = note
                closest_index = idx
                target_freq = freq
        
        return closest_index, closest_string, target_freq, min_diff
    
    @staticmethod
    def get_max_strings(instrument):
        """Get maximum number of strings for instrument"""
        return 6 if instrument == "6" else 8
