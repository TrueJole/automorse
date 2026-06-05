# automorse

Morse code decoder for the [BF1 easter eggs](https://wiki.gamedetectives.net/index.php?title=Battlefield_1#Headphones_and_Morse_code).

## Dependencies

* `numpy`
* `scipy`
* `numba`
* `audio_extract`
* `(pydub)`

## Installation

Download this repository as a .zip file and unpack or execute 
```bash
git clone https://github.com/TrueJole/automorse.git
```

There run 
```bash
pip install -r requirements.txt
```

## Usage

This code is intended for any audio or video files, with Morse transmitted at 20 wpm. To use, run `python main.py [PATH_TO_FILE]` in the command line. A few characters may be wrong due to noise in the recording. The first run of the program will be slower than usual due to the creation of a `numba` JIT cache for the spectrogram subroutine.

### Example

```bash
> python main.py ~/Downloads/example.mp4
Success : audio file has been saved to "/tmp/tmpeklkftg8.wav".
GUWTVMEEWLALJDNACOMHOCRQFHYLFWLHZAJHRHIIVVIQAMZHWFWNSHGOKTYHHDOACOMHOACZEBOUJHMGGUWTVMEEWLALJDN H


AN ESCALATION:
Most likely first letter: A : 1  ( 50 %)
Most likely fives:  : 0  ( 0 %)


A BEGINNING:
[1.0, 'CRATE JABAL JIFAR', 'GUWTVMEEWLALJDN', 'https://bf1morse.leonlarsson.com/locations/jifar2.png', 'Sinai Desert', '7']
[0.5161290322580645, 'CRATE TRENCH CANAL', 'GUWTVWVHJCYFEQWL', 'https://bf1morse.leonlarsson.com/locations/canal1.png', 'Suez', '7']
[0.4242424242424242, 'CRATE SEREN VENETIAN', 'GUWTVVIUANMHRHPIRQ', 'https://bf1morse.leonlarsson.com/locations/venetian1.png', 'Monte Grappa', '7']

(🤖100%) (Stage 7) CRATE JABAL JIFAR: Sinai Desert | https://bf1morse.leonlarsson.com/locations/jifar2.png

```

## Algorithm

1. Stereo audio is preprocessed to mono by taking the mean of all tracks.
2. Frequency is detected using the peak of the [periodogram](https://en.wikipedia.org/wiki/Periodogram) (power spectral density) of the audio data.
3. The [spectrogram](https://en.wikipedia.org/wiki/Spectrogram) is computed every 64 samples as the norm square of the [STFT](https://en.wikipedia.org/wiki/Short-time_Fourier_transform), using a [Hann window](https://en.wikipedia.org/wiki/Hann_function) with width 2048. This is evaluated at the frequency detected in step 2.
4. The spectrogram is thresholded at half of its mean to convert it to a binary signal.
5. The times at which the signal changes are computed.
6. The wpm of the Morse code is detected using a least-squares fit to $\mathop{\mathrm{min}}\left(\left|t-\delta t\right|,\left|t-3\delta t\right|,\left|t-7\delta t\right|\right)$, where $t$ is the time between signal changes. The wpm is computed as $\frac{1200}{\delta t}$.
7. Discarding any $t<\frac{\delta t}{2}$ as noise, the signal is parsed into a Morse code string.
8. The Morse code string is decoded to plaintext.

## TODO

1. Add automatic decryption for BF1 An Omen easter egg cipher
2. Port everything to a web app
3. Improve sensitivity for low S/N ratio data
4. Improve documentation
