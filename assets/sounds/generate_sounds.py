"""
Generates simple WAV files (no external downloads needed)
"""

import wave
import struct
import math


def create_tone(filename, freq, duration, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)

    wav = wave.open(filename, "w")
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    for i in range(n_samples):
        value = int(volume * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
        wav.writeframes(struct.pack("<h", value))

    wav.close()


# 🍎 eat sound (short high beep)
create_tone("eat.wav", 880, 0.1)

# 💀 crash sound (low tone)
create_tone("crash.wav", 220, 0.3)

print("Sounds generated!")