"""
As we vary dictionary size, we need to have a way to index our words. 
They change over time
"""

with open('wlist','r') as win:
	wlist = win.readlines()[2:]

dictionary = [ (wlist.index(w), w) for w in wlist]

with open('word_index.txt','w+') as wout:
	for indx, word in dictionary:
		wout.write("{} : {}\n".format(indx, word))

