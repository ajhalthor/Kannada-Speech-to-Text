#!/usr/bin/python
# -*- coding: utf8 -*-
"""
We want the context dependent nature of triphones, however with limited sparse data like monophones.
Hence we use Syllable based modeling. Furthermore, Kannada is a Syllable based language. 

1. Get syllables for every dictionary word using dict_syl.txt.
2. For Every Syllable in every word, get the corrusponding triphone sequence.
	E.g.
		ತ = ತ್+ಅ 
		ಪುಂ = ಪ್+ಉ ಪ್-ಉ+ಮ್ ಉ-ಮ್

3. Output these sequences to dict_tri
4. Create fulllist0 which is the list of all triphones used
"""
import tokens
import re 

"""Get all tokens of the Kannada language and categorize them in lists."""
vowels, consonants, alankars = read_token_files()

"""Get syllables of all words in `dict_syl.txt` as a list."""
syl_dict = get_syllables_all_words()

all_tris = []
for word, syls in syl_dict:
	tri_list = []
	for s in syls:

		"""Get tokens list of the syllable"""
		tokens = get_tokens(s)

		"""Get monophone sequence of the syllable"""
		monos = get_monophones(tokens, vowels, consonants, alankars)

		"""Create trihpone sequence of the syllable"""
		tris = get_triphones(word, monos)

		tri_list.extend(tris)

	all_tris.append((word,tri_list))

#Replace syllables with constitutent trihpones for every syllable in word
with open('dict-tri','w+') as t:
	t.write("SENT-END\t\t\tsil\nSENT-START\t\t\tsil\n")
	for word, tri_list in all_tris:
		tri_list.append('sp')
		tri_str = ' '.join(tri_list)
		t.write("{}\t\t\t{}\n".format(word, tri_str))

#List of all triphones (from syllables) constitutes `fulllist0`.
all_triphones = []
for word, tri_list in all_tris:
	all_triphones.extend(tri_list)

with open('fulllist0','w+') as f:
	all_triphones = list(set(all_triphones))
	for tri in all_triphones:
		f.write("{}\n".format(tri))
	f.write("sil\n")
	