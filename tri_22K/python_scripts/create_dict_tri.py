#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Create a triphone dictionary file.

1. Read dict
2. From line 3, split lines with respect to '\t\t\t'. We should get 3 items per line 
3. Delete 2nd item. For the 3rd, put the phones into a list (length n) and delete last element "sp" 
4. 
	For [0]th element of new triphone  ==> take [0]+[1]

	for i in range(2,len(ph_arr)): original[i-2]-original[i]+original[i]

	For [n]th element of new triphone  ==> take [n-2]-[n-1]

5. append 'sp'

6. Write the 1st item and this new triphone array to dict-tri
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
	tri = []
	if len(mono) == 1: 
		tri_dict.append( (word,[mono[0], 'sp']) )
		continue

	tri.append( mono[0]+"+"+mono[1])

	for i in range(2,len(mono)):
		tri.append(mono[i-2]+"-"+mono[i-1]+"+"+mono[i])

	tri.append(mono[len(mono)-2]+"-"+mono[len(mono)-1] )
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




