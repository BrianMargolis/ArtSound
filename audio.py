import librosa

from image import Image


class Audio:
    def __init__(self, image: Image, sr=44100):
        self.image = image
        self.sr = sr
        self.y = librosa.istft(image.edges.img)
        self.path = "{0}.wav".format(image.name)
        self.write()

    def write(self):
        librosa.output.write_wav(self.path, self.y, sr=self.sr)

    @property
    def duration(self):
        return len(self.y) / self.sr