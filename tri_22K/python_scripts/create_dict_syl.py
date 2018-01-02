#!/usr/bin/python
# -*- coding: utf8 -*-
"""
From the word list `wlist`, this program creates the vocab list OR input dictionary with corresponding  syllable sequences.

"""
from tokens import read_token_files, get_tokens, get_syllables
import re 

fout = open('dict_syl.txt','w+')

words = []
with open('wlist','r') as win:
	for line in win.readlines()[2:]:
		word = line.strip()
		words.append(word)

all_syls = [] #For (word, syllable) tuple
syls = [] #Storing all syllables

"""Get all tokens of the Kannada language and categorize them in lists."""
vowels, consonants, alankars = read_token_files()

for word in words:
	"""Get tokens of word input."""
	tokens = get_tokens(word)

	"""Get constitutent syllables of the word."""
	syllables = get_syllables(tokens, vowels, consonants, alankars)

	all_syls.append( (word,syllables) )
	syls.extend( syllables )

#Create Syllable dictionary
with open('dict_syl.txt','w+') as dout:
	for word, syls_list in all_syls:
		syls_list.append('sp')
		syls_str = ' '.join(syls_list)
		dout.write("{}\t\t\t[{}]\t\t\t{}\n".format(word,word,syls_str))

#Retain only unique syllables
syls = list(set(syls))

#Create a syllable file with all syllables encountered
with open('syllables1','w+') as fs:
	for s in syls:
		fs.write("{}\n".format(s))
	fs.write("sil\n")
