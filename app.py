import matplotlib.pyplot as plt
import moviepy.editor as mpy

from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# Load video and audio
video = mpy.VideoFileClip("video.MP4")

# Load audio
audio_segment = AudioSegment.from_file('video.MP4', format="mp4")

# Detect non-silent parts
nonsilent_parts = detect_nonsilent(
    audio_segment,
    min_silence_len=2000,  # minimum length of silence (in milliseconds)
    silence_thresh=-50,  # silence threshold (in dB)
)

# Generate waveform data
waveform = audio_segment.get_array_of_samples()
times = [float(i) / audio_segment.frame_rate for i in range(len(waveform))]

# Plot waveform
plt.figure(figsize=(20, 4))
plt.plot(times, waveform, color="gray")

final_video = None
final_audio = []

# Highlight silent parts
for start, end in nonsilent_parts:
    plt.axvspan(start / 1000, end / 1000, color="red", alpha=0.3)
    clip = video.subclip(start / 1000, end / 1000)
    final_video = (
        clip if final_video is None else mpy.concatenate_videoclips([final_video, clip])
    )
    final_audio.append(clip.audio)

# Concatenate audio clips
final_audio_clips = mpy.concatenate_audioclips(final_audio)

if final_video is not None:
    final_video = final_video.set_audio(final_audio_clips)
    final_video.write_videofile('final_video.mp4', audio_codec='aac')
else:
    print("No nonsilent parts were detected. The final video will not be created.")

plt.title("Audio Waveform with Highlighted Silent Sections")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.show()
