"""
Create test.scp
"""
import os 

with \
	open('short/wlist_short.txt','r') as win, \
	open('short/test_short.scp','w+') as tout:
		wlist = [w.strip() for w in win.readlines()]
		for w in wlist:
			tout.write("test_samples/{}_.wav\n".format(w))
