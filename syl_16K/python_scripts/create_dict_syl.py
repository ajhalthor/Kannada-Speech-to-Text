#!/usr/bin/python
# -*- coding: utf8 -*-
"""
From the word list `wlist`, this program creates the vocab list OR input dictionary with corresponding  syllable sequences.

"""
import tokens
import re 

fout = open('dict_syl.txt','w+')

words = []
with open('wlist','r') as win:
	for line in win.readlines()[2:]:
		word = line.strip()
		words.append(word)

all_syls = []

"""Get all tokens of the Kannada language and categorize them in lists."""
vowels, consonants, alankars = read_token_files()

for word in words:
	"""Get tokens of word input."""
	tokens = get_tokens(word)

	"""Get constitutent syllables of the word."""
	syllables = get_syllables(tokens, vowels, consonants, alankars)

	all_syls.extend( (word,syllables) )

#Create Syllable dictionary
with open('dict_syl.txt','w+') as dout:
	for word, syls in all_syls:
		syls.append('sp')
		syls_str = ' '.join(syls_list)
		dout.write("{}\t\t\t[{}]\t\t\t{}\n".format(word,word,syls_str))

#Retain only unique syllables
all_syls = list(set(all_syls))

#Create a syllable file with all syllables encountered
with open('syllables1','w+') as fs:
	for s in all_syls:
		fs.write("{}\n".format(s))
	fs.write("sil\n")
