from typing import List

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.video import VideoClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import clips_array

from audio import Audio
from image import ImageFromPath, Image

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", type=str,
                        help="A path to the image you want to sonify")
    parser.add_argument("-s", "--sample_rate", default=44100, type=int,
                        help="Sample rate of the audio in Hz. Defaults to 44.1kHz.")
    parser.add_argument("-f", "--frame_rate", default=30, type=int,
                        help="Frame rate of the video output in frames per second. Defaults to 30.")
    parser.add_argument("-d", "--display", default="both", type=str, choices=["edges", "original", "both"],
                        help="Whether to show the edges of the image, the unprocessed image, or both side-by-side. Defaults to both.")
    parser.add_argument("-t", "--threshold", default=(150, 250), type=int, nargs=2, help="Threshold values for edge detection. Defaults to (150, 250).")

    args = vars(parser.parse_args())
    path = args['image_path']
    frame_rate = args['frame_rate']
    display = args['display']
    sr = args['sample_rate']

    image = ImageFromPath(path)
    image.edge_detection()
    audio = Audio(image, sr)

    if display == "edges":
        frames = animate_frames(image.edges, audio.duration, frame_rate)
        final_clip = render_clip(frames, audio, frame_rate)
    elif display == "original":
        frames = animate_frames(image, audio.duration, frame_rate)
        final_clip = render_clip(frames, audio, frame_rate)
    elif display == "both":
        edge_frames = animate_frames(image.edges, audio.duration, frame_rate)
        edge_clip = render_clip(edge_frames, audio, frame_rate)

        original_frames = animate_frames(image, audio.duration, frame_rate)
        original_clip = render_clip(original_frames, audio, frame_rate)

        final_clip = clips_array([[edge_clip, original_clip]])

    final_clip.write_videofile("{0}.mp4".format(image.name))


def animate_frames(base_image: Image, duration: float, frame_rate: int) -> List[Image]:
    frames = []
    n_frames = int(duration * frame_rate)
    vertical_bar = ImageFromPath("vertical_bar.png")
    vertical_bar.resize_to_match(base_image, height=True)  # stretch the vbar to the height of the image
    base_image.to_bgr()
    for i in range(n_frames):
        percent = i / n_frames
        x = int(percent * base_image.width())
        frame = base_image.overlay(vertical_bar, 1, 1, x, 0)
        frames.append(frame)
    return frames


def render_clip(frames, audio, framerate) -> VideoClip:
    clips = []
    clip_duration = 1 / framerate
    for frame in frames:
        clip = ImageClip(frame.img)
        clip = clip.set_duration(clip_duration)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips, method="chain")
    final_clip = final_clip.set_audio(AudioFileClip(audio.path))
    final_clip = final_clip.set_fps(framerate)
    return final_clip


if __name__ == "__main__":
    main()
