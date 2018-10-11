import cv2 as cv
import librosa
import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip

from moviepy.editor import concatenate_videoclips
from moviepy.video.VideoClip import ImageClip


def get_frames(edges, l, framerate=60):
    frames = []
    n_frames = int(l * framerate)
    vertical_bar = cv.imread("vertical_bar.png")
    vertical_bar = cv.cvtColor(vertical_bar, cv.COLOR_BGR2GRAY)  # make the vbar 1-channel
    h = edges.shape[0]
    w = vertical_bar.shape[1]
    vertical_bar = cv.resize(vertical_bar, (w, h))  # stretch the vbar to the height of the image
    for i in range(n_frames):
        percent = i / n_frames
        frame = stack(edges, vertical_bar, percent)
        cv.imwrite("frames/{0}.png".format(i), frame)
        frames.append(frame)
    return frames


def stack(edges, vertical_bar, percent):
    necessary_padding = edges.shape[1] - vertical_bar.shape[1]
    height = vertical_bar.shape[0]
    l_padding = int(percent * necessary_padding)
    r_padding = necessary_padding - l_padding
    padded_bar = np.concatenate((np.zeros((height, l_padding)),
                                 vertical_bar,
                                 np.zeros((height, r_padding))),
                                axis=1)
    frame = 1 * edges + 1 * padded_bar
    return cv.merge((frame, frame, frame))  # make the frame 3-channel


def main(name):
    # do edge detection
    edges, edge_file_name = edge_detect(name)

    # invert spectrogram
    y = invert(edges)

    # get signal length and make frames
    l = signal_len(y)
    frames = get_frames(edges, l)
    cv.imshow("asdf", frames[0])

    audio = AudioFileClip("output.wav")
    clips = []
    for frame in frames:
        clip = ImageClip(frame)
        clip = clip.set_duration(1 / 60)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips, method="chain")
    final_clip = final_clip.set_audio(audio)
    final_clip = final_clip.set_fps(60)
    final_clip.write_videofile("{0}.mp4".format(name.rstrip(".jpg").rstrip(".png")))


def invert(edges, sr=44100):
    # invert spectrogram
    y = librosa.istft(edges)
    librosa.output.write_wav("output.wav", y, sr=sr)
    return y


def edge_detect(name):
    # load an image
    img = cv.imread('{0}'.format(name), 0)
    # edge detection
    edges = cv.Canny(img, 150, 250)
    edge_file_name = '{0}_edges.jpg'.format(name.rstrip(".jpg"))
    cv.imwrite(edge_file_name, edges)
    return edges, edge_file_name


def signal_len(y, sr=44100):
    n_samples = len(y)
    return n_samples / sr


if __name__ == "__main__":
    main('goat.jpg')
