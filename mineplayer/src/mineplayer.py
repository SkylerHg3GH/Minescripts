# -*- encoding: UTF-8 -*-
import sys
import cv2
import json
import time
import threading
from pathlib import Path
import pygame
import minescript as m

def to_hex_rgb(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def format_time(seconds):
    minutes = str(int(seconds // 60)).rjust(2, '0')
    secs = str(int(seconds % 60)).rjust(2, '0')
    return f"{minutes}:{secs}"

MAX_BLOCKS_PER_ROW = 35
VIDEO_HEIGHT = 19
PROGBAR_WIDTH = 20

video_path = Path(sys.argv[1])
audio_path = Path(sys.argv[2]) if len(sys.argv) > 2 else video_path.with_suffix(".mp3")
pygame.mixer.init()
def play_audio(path):
    if path.exists():
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play()
threading.Thread(target=play_audio, args=(audio_path,), daemon=True).start()
cap = cv2.VideoCapture(str(video_path))
if not cap.isOpened():
    print("Cannot open video:", video_path)
    sys.exit(1)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_delay = 1.0 / fps if fps > 0 else 1/30
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
video_duration_seconds = total_frames / fps
frame_idx = 0
start_time = time.time()
screen = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (MAX_BLOCKS_PER_ROW, VIDEO_HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    current_frame = [' ']
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            current_frame.append({
                "text": "█",
                "color": to_hex_rgb(tuple(frame[y, x]))
            })
    screen = current_frame
    current_video_time = time.time() - start_time
    progress_fraction = min(current_video_time / video_duration_seconds, 1.0)
    progress_blocks = int(progress_fraction * PROGBAR_WIDTH)
    screen.append({'text': '-' * progress_blocks, "color": '#FF0000'}) 
    screen.append('⬤')
    screen.append({'text': ('-' * (PROGBAR_WIDTH - progress_blocks - 1) + ' '), 'color': '#FF0000'})
    total_time_str = format_time(video_duration_seconds)
    current_time_str = format_time(current_video_time)
    screen.append(current_time_str + "/" + total_time_str)
    m.echo_json(json.dumps(screen)) 
    frame_idx += 1
    target_time = start_time + frame_idx * frame_delay
    now = time.time()
    sleep_time = target_time - now
    if sleep_time > 0:
        time.sleep(sleep_time)

cap.release()
