# Speech-to-Text on Raspberry Pi 5 with I2S Microphone and Whisper

This project implements speech-to-text transcription on a Raspberry Pi 5 using an I2S MEMS microphone and the OpenAI Whisper model. It features a fullscreen Pygame interface for easy recording and transcription.


## Features

- I2S MEMS microphone support on Raspberry Pi 5
- Simple fullscreen UI (Pygame) for recording and viewing transcriptions
- Accurate speech recognition using OpenAI Whisper
- Real-time audio capture and processing


## Hardware Requirements

- Raspberry Pi 5
- I2S MEMS microphone (e.g., INMP441)
- MicroSD card with Raspberry Pi OS


## Software Requirements

- Python 3.9+
- `pygame`
- `pyaudio`
- `whisper` (OpenAI Whisper)
- Raspberry Pi OS (Bookworm or later recommended)


## Configure I2S Microphone on Raspberry Pi 5

Open a terminal and run:
```
git clone https://github.com/PaulCreaserML/rpi-i2s-audio
cd rpi-i2s-audio
dtc -I dts -O dtb -o rpi-i2s-mic.dtbo rpi-i2s-mic.dts
sudo cp rpi-i2s-mic.dtbo /boot/overlays/.
sudo nano /boot/firmware/config.txt
```

In `config.txt`:
- Comment out `dtparam=audio=on`
- Uncomment `dtparam=i2s=on`
- Add: `dtoverlay=rpi-i2s-mic`

Save and exit (`Ctrl + O`, `Enter`, then `Ctrl + X`), then reboot (`sudo reboot now`)

Use `arecord -l` to check if the mic is detected as a soundcard.


## Application Interface
- The interface will launch in fullscreen.
- Click "Record" to capture audio.
- Transcription will appear after recording.


## Troubleshooting

- Ensure the microphone is wired to the correct I2S pins.
- If `arecord -l` does not show a soundcard, check your `config.txt` and overlay steps.
- Confirm all Python dependencies are installed and compatible.

---


*Credits: I2S overlay and setup adapted from PaulCreaserML/rpi-i2s-audio.*



