"""
Audio processing module
Handles microphone input and pitch detection using autocorrelation
"""

import numpy as np
import pyaudio
from config import NUM_SAMPLES, SAMPLING_RATE, MIC_DEVICE_INDEX


class AudioProcessor:
    """Manages audio input and pitch detection"""
    
    def __init__(self):
        # Initialize PyAudio
        self.pa = pyaudio.PyAudio()
        
        # Open audio input stream
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLING_RATE,
            input=True,
            frames_per_buffer=NUM_SAMPLES,
            input_device_index=MIC_DEVICE_INDEX
        )
    
    def detect_pitch(self):
        """
        Detect the fundamental frequency from microphone input
        Returns: frequency in Hz, or 0 if detection fails
        """
        if self.stream.get_read_available() < NUM_SAMPLES:
            return 0
        
        # Read raw data from microphone
        data = self.stream.read(NUM_SAMPLES, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.int16) / 32768.0
        
        # Detect pitch using autocorrelation
        return self._autocorrelation(audio, SAMPLING_RATE)
    
    def _autocorrelation(self, signal, rate):
        """
        Estimate fundamental frequency using autocorrelation method
        
        Args:
            signal: Audio signal array
            rate: Sampling rate in Hz
        
        Returns:
            Detected frequency in Hz
        """
        # Remove DC offset
        signal = signal - np.mean(signal)
        
        # Compute autocorrelation
        corr = np.correlate(signal, signal, mode='full')[len(signal) - 1:]
        
        # Find the first peak
        d = np.diff(corr)
        if len(d) == 0:
            return 0
        
        start = np.where(d > 0)[0]
        if len(start) == 0:
            return 0
        
        peak = np.argmax(corr[start[0]:]) + start[0]
        
        # Calculate frequency
        return rate / peak if peak != 0 else 0
    
    @staticmethod
    def freq_to_cents(detected_freq, target_freq):
        """
        Calculate the logarithmic difference between frequencies in cents
        
        Args:
            detected_freq: Detected frequency in Hz
            target_freq: Target frequency in Hz
        
        Returns:
            Difference in cents, or None if invalid
        """
        if detected_freq == 0:
            return None
        return 1200 * np.log2(detected_freq / target_freq)
    
    def cleanup(self):
        """Stop audio stream and clean up resources"""
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
