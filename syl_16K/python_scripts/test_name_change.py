"""
Rename sample WAV files in `test_samples` and `recorded_test_samples`. 

The names were changed from numeric IDs to actual word names using word_index.txt.
"""
import os

wlist = []
with open('word_index.txt','r') as win:
	for line in win.readlines():
		index, word = line.split(' : ')
		index = index.strip()
		word = word.strip()
		wlist.append( (index, word) )


test_samples = [(name.split('.')[0].split('_')[0], name.split('.')[0]) for name in os.listdir('recorded_test_samples') if name.endswith('wav')]

for index, sample in test_samples:
	#For words with multiple test samples
	version = sample.split('_')[1]
	if len(version):
		os.rename("recorded_test_samples/{}.wav".format(sample), "recorded_test_samples/{}_{}.wav".format([w for i, w in wlist if i == index][0], version))
	else:
		os.rename("recorded_test_samples/{}.wav".format(sample), "recorded_test_samples/{}_.wav".format([w for i, w in wlist if i == index][0]))
