#!/usr/bin/python
# -*- coding: utf8 -*-
"""
From the word list `wlist`, create the vocab list OR input dictionary of constituent monophone sequences.

"""
import tokens

words = []
with open('wlist','r') as win:
	for line in win.readlines()[2:]:
		word = line.strip()
		words.append(word)

"""Get all tokens of the Kannada language and categorize them in lists."""
vowels, consonants, alankars = read_token_files()

all_phones = []

for word in words:

	"""Get token list of corresponding word"""
	tokens = get_tokens(word)

	"""Get monophone list using token list"""
	phonemes = get_monophones(tokens,vowels, consonants, alankars)

	all_phones.append( (word, phonemes) )


#Create Monophone dictionary
with open('dict','w+') as dout:
	dout.write("SENT-END\t\t\t[]\t\t\tsil\nSENT-START\t\t\t[]\t\t\tsil\n")

	for word, phs_list in all_phones:
		phs_list.append('sp')
		phs_str = ' '.join(phs_list)
		dout.write("{}\t\t\t[{}]\t\t\t{}\n".format(word,word,phs_str))

