#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Cannot perform convert syllables to monophones normally because triphones arent the same as the syllables. 

1. Read dict-tri and store in list of (word, triphone)
3. Read prompts.txt. Retrieve the corrusponding triphones from the dictionary for every word encountered
(sample, tri_sequence)
2. Write to an MLF file called wintri.mlf in the same format with every triphone on a line

triphones1 is the same as fulllist0

"""
import re

dict_list = []
with open('dict-tri','r') as din:
	for line in din.readlines()[2:]:
		word, tri_sequence = line.split('\t\t\t')
		dict_list.append( (word.strip(), tri_sequence.strip()) )

with open('prompts.txt','r') as pin, open('wintri.mlf','w+') as wout :
	wout.write('#!MLF!#\n')
	for line in pin.readlines():
		sample, sentence = line.split(' ', 1)
		sample = sample.strip()
		sentence = sentence.strip()
		wout.write("\"{}.lab\"\nsil\n".format(sample))
		words = sentence.split(' ')
		for w in words:
			tri_sequence = [tri for word, tri in dict_list if word==w][0]
			tri_sequence = tri_sequence.strip()

			tri_words = re.findall(r"[^-+ ]+", tri_sequence)
			tri_del = re.findall(r"[-+ ]+",tri_sequence)
			tri_del.append('')
			new_sequence = [val for pair in zip(tri_words, tri_del) for val in pair]

			for tri in new_sequence:
				if tri == ' ':
					wout.write("\n")
				else:
					wout.write(tri)
			wout.write("\n")
		wout.write("sil\n.\n")

with open('triphones1','w+') as tout:
	all_syls = list(set([y for x in dict_list for y in x[1].split(' ') ]))
	for s in all_syls:
		tout.write("{}\n".format(s))
	tout.write("sil\n")
