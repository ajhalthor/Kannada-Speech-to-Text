#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Create a triphone dictionary file from monohpones of words.

1. Read dictionary of monophones `dict`.
2. From line 3, split lines with respect to `\t\t\t`. We should get 3 items per line:
	- Word Internal Representation 
	- Word External Representation
	- Monohpone Sequence

3. Put the phones into a list and delete last element "sp" 
4. Generate triphone sequence for each word.
5. Write the 1st item and this new triphone array to dict-tri
7. Repeat for other lines

"""
all_tri = []

mono_dict = []
with open('dict','r') as d:
	 for line in d.readlines()[2:]:
	 	line = line.strip()
	 	word , _ , mono =  line.split('\t\t\t')
	 	mono = mono.split(' ')
	 	mono = mono[:-1]
	 	mono_dict.append( (word, mono) )

tri_dict = []
for word, mono in mono_dict:

	"""Get triphones of a given word."""
	tri = get_triphones(word, mono)

	tri.append('sp')

	#Store all triphones to create fulllist0
	all_tri.extend(tri)

	tri_dict.append( (word, tri) )


with open('dict-tri','w+') as t:
	t.write("SENT-END\t\t\tsil\nSENT-START\t\t\tsil\n")
	for word, tri in tri_dict:
		tri_str = ' '.join(tri)
		t.write("{}\t\t\t{}\n".format(word, tri_str))

with open('fulllist0','w+') as f:
	all_tri = list(set(all_tri))
	for tri in all_tri:
		f.write("{}\n".format(tri))




