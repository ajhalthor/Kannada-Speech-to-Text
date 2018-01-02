"""
Create test.scp
"""
import os 

folder = 'short' #Change to short | middle | long
subword = 'mono' #Change to mono | tri | syl

with \
	open('{}/{}/wlist_{}.txt'.format(folder,subword,folder),'r') as win, \
	open('{}/{}/test_{}.scp'.format(folder,subword,folder),'w+') as tout:
		wlist = [w.strip() for w in win.readlines()]
		for w in wlist:
			tout.write("test_samples/{}_.wav\n".format(w))
