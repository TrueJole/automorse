from morse import detect_frequency, spectrogram, parse, decode
from scipy.io.wavfile import read
import argparse
from pathlib import Path

import tools


parser = argparse.ArgumentParser(
    prog = "Morse",
    description = "Decode Morse code from an audio/video file and interprete it as BF1 morse code solutions.",
    epilog = "Hacked together by Daniel Sun - Made worse by jole.k"
)
parser.add_argument("filename", type = Path)
parser.add_argument("-w", "--wpm", type = bool, default = False, help = "Whether to trigger WPM detection.")

parser.add_argument("-f", "--freq", type = bool, default = True, help = "Whether to trigger frequency detection.")

###
parser.add_argument("-a", "--audio", default = False, help = "[DEPRECATED] file is an audio", action='store_true')
parser.add_argument("-v", "--verbose", default = False, help = "print additional information", action='store_true')
parser.add_argument("-s", "--stage", type= int, default = 0, help = "[OPTIONAL] specify an A BEGINNING stage")
###

args = parser.parse_args()
file = args.filename.expanduser().resolve()
detect_wpm = args.wpm
detect_freq = args.freq

###
use_audio = args.audio
tools.verbose = args.verbose

tools.print_verbose("Got file path: ", str(file))

if use_audio:
    # DEPRECATED -v seems to work for audio as well :D

    # Convert all audio to wav
    from pydub import AudioSegment

    extension = str(file).split(".")[-1]

    tools.print_verbose("Converting ", extension, " to .wav")

    # NOTE This will override the old file but keep the old name + extension. Calling this again WILL cause an error
    sound = AudioSegment.from_file(file, extension)
    sound.export(file, format="wav")
else:
    # Convert video to wav audio
    import posixpath
    from audio_extract import extract_audio


    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.wav') as temp_file:
        audiofile = temp_file.name #str(file)
        tools.print_verbose("Converting video to ", audiofile, ".wav")

        #file_path = temp_file.name
        #print(f"Temporary file created at: {file_path}")
        # Write text data
        #temp_file.write("This is a named temporary text file.")

        extract_audio(input_path=file, output_path=audiofile, overwrite=True, output_format="wav")
        file = audiofile #+ ".wav"

###

rate, data = read(file)

###

# Manually delete the temp file
import os
if (not use_audio) and os.path.exists(audiofile):
    os.unlink(audiofile)
    tools.print_verbose(f"Manually deleted: {audiofile}")

###

if data.ndim >= 2:
    data = data.mean(axis = 1) # Convert stereo to mono
if detect_freq:
    F = detect_frequency(data, rate)
    tools.print_verbose(f"Detected frequency: {F} Hz")
else:
    F = 800

spec = spectrogram(data, rate, F)
signal = spec > spec.mean() / 2
morse, wpm = parse(signal, rate, detect_wpm)
if detect_wpm:
    tools.print_verbose(f"Detected WPM: {wpm} wpm")

message = decode(morse)

tools.print_verbose(message)

###

beginning_stage = args.stage

# TODO Split message at . and analyse individually

message = message.strip()

print(message)
print()
print()

import escalation
escalation.escalation(message)

import beginning
#beginning.beginning_better(message, beginning_stage)
beginning.beginning(message, beginning_stage)


###
