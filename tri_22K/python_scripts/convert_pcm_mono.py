"""
Converts input sample as :
1. Transforms to 16,000 Hz sampling rate
2. Convert to PCM wav
3. Convert to mono channel 

Replace the source and destination file names as required:

samples : directory of WAV files of Sample sentences required to be converted.
samples_converted : Conversion of WAV files in `samples` to PCM, mono-channel format for traning.

recorded_test_samples : WAV files of individual words required to be converted.
test_samples : Conversion of WAV files in `recorded_test_samples` to PCM, mono-channel format for testing.

"""
import subprocess
import numpy as np
import os
import wave

source_dir = "recorded_test_samples"
dest_dir = "test_samples"
sample_rate = 22050

def convert_to_pcm_wav(path, file):
	""" Converts file to PCM, mono-channel format"""
	subprocess.check_output(['ffmpeg','-i', path, '-ar', str(sample_rate), '-ac','1', '-acodec','pcm_s16le', os.path.join(dest_dir,file)])


files = []
for root, dirs, files in os.walk(source_dir):
	for file in files:
		if file.endswith('.wav'):
			path = os.path.join(root, file)
			convert_to_pcm_wav(path, file)
