from audio import Audio
from image import ImageFromPath

import argparse

from sonification import Sonification


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
    parser.add_argument("-t", "--threshold", default=(150, 250), type=int, nargs=2,
                        help="Threshold values for edge detection. Defaults to (150, 250).")
    parser.add_argument("-e", "--edges-only", default=False, action='store_const', const=True,
                        help="Don't produce audio or video, just run edge detection. Useful for determining threshold parameters. Defaults to false.")

    args = vars(parser.parse_args())
    path = args['image_path']
    frame_rate = args['frame_rate']
    display = args['display']
    sr = args['sample_rate']
    edges_only = args['edges_only']
    threshold = args['threshold']

    image = ImageFromPath(path)
    image.edge_detection(threshold)
    if not edges_only:
        audio = Audio(image, sr)

        sonification = Sonification(image, audio, display, frame_rate)
        sonification.render()
        sonification.write()


if __name__ == "__main__":
    main()
