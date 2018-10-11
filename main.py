from typing import List

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.video.VideoClip import ImageClip

from audio import Audio
from image import ImageFromPath, Image


def animate(base_image: Image, l: float, frame_rate: int) -> List[Image]:
    frames = []
    n_frames = int(l * frame_rate)
    vertical_bar = ImageFromPath("vertical_bar.png")
    vertical_bar.set_num_channels(1)  # make the vertical bar grayscale
    vertical_bar.resize_to_match(base_image, height=True)  # stretch the vbar to the height of the image
    for i in range(n_frames):
        percent = i / n_frames
        x = int(percent * base_image.width())
        frame = base_image.overlay(vertical_bar, 1, 1, x, 0)
        frame.set_num_channels(3)  # make the frame BGR
        frames.append(frame)
    return frames


def main(path, framerate):
    image = ImageFromPath(path)
    audio = Audio(image)

    frames = animate(image.edges, audio.duration, framerate)

    clips = []
    clip_duration = 1 / framerate
    for frame in frames:
        clip = ImageClip(frame.img)
        clip = clip.set_duration(clip_duration)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips, method="chain")
    final_clip = final_clip.set_audio(AudioFileClip(audio.path))
    final_clip = final_clip.set_fps(framerate)
    final_clip.write_videofile("{0}.mp4".format(image.name))


if __name__ == "__main__":
    main('goat.jpg', 30)
