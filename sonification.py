import logging
from typing import List
import cv2 as cv

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import clips_array
from moviepy.video.compositing.concatenate import concatenate_videoclips

from image import Image, ImageFromPath


class Sonification():
    def __init__(self, image, audio, display, frame_rate):
        self.image = image
        self.audio = audio
        self.display = display
        self.frame_rate = frame_rate
        self.clip = None
        self.vertical_bar_path = "vertical_bar.png"

    def render(self):
        if self.display == "edges":
            self.clip = self._render_clip(self._frames(self.image.edges))
        elif self.display == "original":
            self.clip = self._render_clip(self._frames(self.image))
        elif self.display == "both":
            edge_clip = self._render_clip(self._frames(self.image.edges))
            original_clip = self._render_clip(self._frames(self.image))

            self.clip = clips_array([[edge_clip, original_clip]])

    def _render_clip(self, frames):
        logger = logging.getLogger('logger')
        logger.info("Rendering video...")

        clips = []
        clip_duration = 1 / self.frame_rate
        for frame in frames:
            clip = ImageClip(frame.img)
            clip = clip.set_duration(clip_duration)
            clips.append(clip)
        final_clip = concatenate_videoclips(clips, method="chain")
        final_clip = final_clip.set_audio(AudioFileClip(self.audio.path))
        final_clip = final_clip.set_fps(self.frame_rate)
        return final_clip

    def _frames(self, image) -> List[Image]:
        logger = logging.getLogger('logger')

        frames = []
        n_frames = int(self.audio.duration * self.frame_rate)
        vertical_bar = ImageFromPath(self.vertical_bar_path)
        vertical_bar.resize_to_match(image, height=True)  # stretch the vbar to the height of the image
        if image.is_grayscale:
            image.to_bgr()

        logger.info("Generating {0} frames...".format(n_frames))
        for i in range(n_frames):
            percent = i / n_frames
            x = int(percent * image.width())
            frame = image.overlay(vertical_bar, 1, 1, x, 0)
            cv.imwrite("frames/{0}.png".format(i), frame.img)
            frames.append(frame)
        return frames

    def write(self):
        logger = logging.getLogger('logger')
        logger.info("Writing video to disk...")
        self.clip.write_videofile("{0}.mp4".format(self.image.name), verbose=False)
