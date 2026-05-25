from morse import detect_frequency, spectrogram, parse, decode
from scipy.io.wavfile import read
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    prog = "Morse",
    description = "Decode Morse code from an audio file.",
    epilog = "Hacked together by Daniel Sun"
)
parser.add_argument("filename", type = Path)
parser.add_argument("-w", "--wpm", type = bool, default = False, help = "Whether to trigger WPM detection.")

parser.add_argument("-f", "--freq", type = bool, default = True, help = "Whether to trigger frequency detection.")

###
parser.add_argument("-l", "--long", default = False, help = "Whether to search the whole string or only the first 30 characters", action='store_true')
###

args = parser.parse_args()
file = args.filename.expanduser().resolve()
detect_wpm = args.wpm
detect_freq = args.freq

###

import posixpath
from audio_extract import extract_audio
audiofile = str(file) #posixpath.join(file, ".wav")
print(audiofile)
extract_audio(input_path=file, output_path=audiofile, overwrite=True, output_format="wav")
file = audiofile + ".wav"

###

rate, data = read(file)
if data.ndim >= 2:
    data = data.mean(axis = 1) # Convert stereo to mono
if detect_freq:
    F = detect_frequency(data, rate)
    print(f"Detected frequency: {F} Hz")
else:
    F = 800

spec = spectrogram(data, rate, F)
signal = spec > spec.mean() / 2
morse, wpm = parse(signal, rate, detect_wpm)
if detect_wpm:
    print(f"Detected WPM: {wpm} wpm")

message = decode(morse)

print(message)

###

longSearch = args.long

message = message.strip()
if not longSearch:
    message = message [0:30]

morse = morse.strip()
morse = "-.-. .. - .- .. .-. -.. .- -. .-. .- -... .-.. .-.. .. ...."#morse [0:100]

print(message)

import json
import Levenshtein


with open('beginning.json', 'r') as f:
    maps = json.load(f)

best = []

for map in maps:
    for locationKey in map.keys():
        if "location" in locationKey:
            for cipherKey in map[locationKey].keys():
                if "cipherText" in cipherKey:
                    best.append([Levenshtein.ratio(map.get(locationKey).get(cipherKey), message),map.get(locationKey).get("plainText"), map.get(locationKey).get(cipherKey),  map.get(locationKey).get("mapUrl"), map.get("mapName"), cipherKey[10:]])
                    if Levenshtein.ratio(map.get(locationKey).get(cipherKey), message) > 0.35:
                        print(map.get(locationKey).get("plainText") + " : " + str(Levenshtein.ratio(map.get(locationKey).get(cipherKey), message)));

best.sort(key=lambda x: x[0])

print(best[-1])
print(best[-2])
print(best[-3])

print()
print()

bestGuess = best[-1]
print("(🤖{certainty}%) (Stage {stage}), {plainText}: {map} | {url}".format(certainty = round(bestGuess[0]*100), plainText=bestGuess[1], map=bestGuess[4], url=bestGuess[3], stage=bestGuess[5]))


###
