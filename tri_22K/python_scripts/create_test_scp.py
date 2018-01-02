"""
Create a file withe the list of test samples in `test.scp` from word list `wlist`. The test samples are PCM, mono-channel WAV files of isolated words of a single speaker.
"""
import os 

with \
	open('wlist','r') as win, \
	open('test.scp','w+') as tout:
		wlist = [w.strip() for w in win.readlines()[2:]]
		for w in wlist:
			tout.write("test_samples/{}_.wav\n".format(w))
