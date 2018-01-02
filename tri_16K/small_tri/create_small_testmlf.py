"""Create testref.mlf"""

import os

folder = 'long'
subword = 'tri'

with \
	open('{}/{}/wlist_{}.txt'.format(folder, subword, folder),'r') as win, \
	open('{}/{}/testref_{}.mlf'.format(folder, subword, folder),'w+') as tout:
		wlist = [w.strip() for w in win.readlines()]
		tout.write("#!MLF!#\n")
		for sample in wlist:
			tout.write("\"*/{}_.lab\"\n".format(sample))
			tout.write("sil\n{}\nsil\n.\n".format(sample.split('_')[0]))
