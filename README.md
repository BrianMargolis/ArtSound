# ArtSound
Sonifies images by running edge detection and then reinterpreting the edges as a spectrogram. The end result of running this program is a video that shows how the sound changes as the image plays left-to-right.

## Installation
First, clone the repo. Then, in a virtual environment:
```
pip install -r requirements.txt
```

## Usage
``` 
python artsound.py [image_path]
```
For detailed information on each CLI option,
``` 
python artsound.py -h
```

## Troubleshooting
#### Memory Issues
If you run out of memory while rendering a movie, try the following steps:
* Decrease frame rate, or increase sample rate (note that increasing sample rate will change the audio)
* Decrease the resolution of the input image
* If you're using 32-bit Python, try switching to 64-bit. If the constraint is not your system (i.e. you have available RAM when the memory error occurs), it could be the limit imposed on Python processes. This limit is higher for 64-bit Python.

## Contribution
If you have an issue with this software, please file an issue on this repository. If you're interested in contributing, please feel free to submit a pull request!

## Credit
Inspiration for this project came from Fatemeh Pishdadian's similar sonification of [Kurt Seligmann's Magnetic Mountain](http://www.artic.edu/aic/collections/artwork/62323).