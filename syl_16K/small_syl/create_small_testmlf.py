""" Creates testref.mlf used that has the word transcriptions for every WAV file in the `test_samples` directory.
This is used for comparing results using HVite.

"""

import os

"""Determine category of words in Dictionay"""
folder = 'short' #Change to short | middle | long
subword = 'mono' #Change to mono | tri | syl

with \
	open('{}/{}/wlist_{}.txt'.format(folder, subword, folder),'r') as win, \
	open('{}/{}/testref_{}.mlf'.format(folder, subword, folder),'w+') as tout:
		wlist = [w.strip() for w in win.readlines()]
		tout.write("#!MLF!#\n")
		for sample in wlist:
			tout.write("\"*/{}_.lab\"\n".format(sample))
			tout.write("sil\n{}\nsil\n.\n".format(sample.split('_')[0]))
