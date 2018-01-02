"""
Creates testref.mlf used that has the word transcriptions for every WAV file in the `test_samples` directory.
This is used for comparing results using HVite.

"""

import os

with \
	open('wlist','r') as win, \
	open('testref.mlf','w+') as tout:
		wlist = [w.strip() for w in win.readlines()[2:]]
		tout.write("#!MLF!#\n")
		for sample in wlist:
			tout.write("\"*/{}_.lab\"\n".format(sample))
			tout.write("sil\n{}\nsil\n.\n".format(sample.split('_')[0]))
