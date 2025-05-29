import os
import wave
import time

import pygame
import pyaudio
import whisper

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_WIDTH, WINDOW_HEIGHT = 480, 320
FPS = 30

# Audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 16 kHz for Whisper
AUDIO_FILE = "temp.wav"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# ─────────────────────────────────────────────────────────────────────────────
# Initialization
# ─────────────────────────────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Speech → Text")
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

# Load Whisper model
model = whisper.load_model("small")
print("Loaded Whisper ‘small’ model.")

# Button rectangle (centered near bottom)
BUTTON_W, BUTTON_H = 120, 48
button_rect = pygame.Rect(
    (WINDOW_WIDTH - BUTTON_W) // 2,
    WINDOW_HEIGHT - BUTTON_H - 20,
    BUTTON_W,
    BUTTON_H,
)

# ─────────────────────────────────────────────────────────────────────────────
# State variables
# ─────────────────────────────────────────────────────────────────────────────
running = True
recording = False
transcribing = False
transcription = ""

# Audio objects (filled when recording starts)
pa = None
stream = None
frames = []

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_ui(status: str = "", transcription: str = "", recording: bool = False):
    screen.fill(BLACK)

    # Draw transcription (when idle and we have text)
    if not recording and not status and transcription:
        # wrap text into lines
        words = transcription.split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] < WINDOW_WIDTH - 20:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)

        y = 20
        for ln in lines[:8]:
            txt = font.render(ln, True, WHITE)
            screen.blit(txt, (10, y))
            y += 34

    # Draw status (centered)
    if status:
        txt = font.render(status, True, WHITE)
        r = txt.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(txt, r)

    # Draw button (Record or Stop)
    if recording:
        color = RED
        label = " Stop "
    elif transcribing:
        color = GRAY
        label = "…"
    else:
        color = GREEN
        label = "Record"

    pygame.draw.rect(screen, color, button_rect)
    btn_txt = font.render(label, True, BLACK)
    br = btn_txt.get_rect(center=button_rect.center)
    screen.blit(btn_txt, br)

    pygame.display.flip()


# ─────────────────────────────────────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────────────────────────────────────
while running:
    # 1) Event handling
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            running = False

        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if button_rect.collidepoint(ev.pos):
                # Clicked our toggle button
                if not recording and not transcribing:
                    # Start recording
                    pa = pyaudio.PyAudio()
                    stream = pa.open(format=FORMAT,
                                     channels=CHANNELS,
                                     rate=RATE,
                                     input=True,
                                     frames_per_buffer=CHUNK)
                    frames = []
                    recording = True
                    transcription = ""  # clear old text
                elif recording:
                    # Stop recording
                    recording = False
                    stream.stop_stream()
                    stream.close()
                    pa.terminate()

                    # Save WAV
                    wf = wave.open(AUDIO_FILE, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()

                    # Move to transcription
                    transcribing = True

    # 2) Recording logic (capture audio in realtime)
    if recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        draw_ui(status="Recording…", recording=True)

    # 3) Transcribe once recording just stopped
    elif transcribing:
        draw_ui(status="Transcribing…")
        # small delay to let the UI update
        pygame.time.delay(200)

        # run whisper
        result = model.transcribe(AUDIO_FILE)
        transcription = result.get("text", "").strip()

        # clean up
        try:
            os.remove(AUDIO_FILE)
        except OSError:
            pass

        transcribing = False

    # 4) Idle: show record button + last transcription
    else:
        draw_ui(transcription=transcription)

    clock.tick(FPS)

pygame.quit()
