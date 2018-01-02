"""
1. Read wlist 
2. Sort based on word length
3. Reduce size to 500 words
	CASE 1: Remove smallest 250 words
	CASE 2: Remove middle 250 words
	CASE 3: Remove last 250 words
4. Sort based on alphabetical order
5. Get monophone sequence of each from dict
6. Write the 500 words with sequences into new dictionary "dict_small_short.txt" | dict_small_middle.txt | dict_small_large.txt
7. Modify the test.scp to include only samples from this new dictionary


"""
subword = 'tri'

#Read wlist
with open('../wlist','r') as win:
	wlist = win.readlines()[2:]

#Sort based on word length
sorted_wlist = sorted(wlist, key=len)

#Reduce size to 500 words
short_wlist = [w.strip() for w in sorted_wlist[:500]]
middle_wlist = [w.strip() for w in sorted_wlist[125:-125]]
long_wlist = [w.strip() for w in sorted_wlist[250:]]

#Sort based on alphabetical order
short_wlist = sorted(short_wlist)
middle_wlist = sorted(middle_wlist)
long_wlist = sorted(long_wlist)

with open('short/{}/wlist_short.txt'.format(subword),'w+') as wout:
	for w in short_wlist:
		wout.write("{}\n".format(w))

with open('middle/{}/wlist_middle.txt'.format(subword),'w+') as wout:
	for w in middle_wlist:
		wout.write("{}\n".format(w))

with open('long/{}/wlist_long.txt'.format(subword),'w+') as wout:
	for w in long_wlist:
		wout.write("{}\n".format(w))

new_dict = []
with open('../dict-tri','r') as din:
	dictionary = din.readlines()[2:]
	for entry in dictionary:
		word,  ph_sequence = entry.split('\t\t\t')
		new_dict.append((word.strip(), ph_sequence.strip()))

dict_small_short_list = [tup for tup in new_dict if tup[0] in short_wlist]
dict_small_middle_list = [tup for tup in new_dict if tup[0] in middle_wlist]
dict_small_long_list = [tup for tup in new_dict if tup[0] in long_wlist]

dict_small_short_list = sorted(dict_small_short_list, key=lambda x: x[0])
dict_small_middle_list = sorted(dict_small_middle_list, key=lambda x: x[0])
dict_small_long_list = sorted(dict_small_long_list, key=lambda x: x[0])

with open("short/{}/dict_short.txt".format(subword),"w+") as sout:
	sout.write("SENT-END\t\t\tsil\nSENT-START\t\t\tsil\n")
	for word, ph_sequence in dict_small_short_list:
		sout.write("{}\t\t\t{}\n".format(word, ph_sequence))

with open("middle/{}/dict_middle.txt".format(subword),"w+") as sout:
	sout.write("SENT-END\t\t\tsil\nSENT-START\t\t\tsil\n")
	for word, ph_sequence in dict_small_middle_list:
		sout.write("{}\t\t\t{}\n".format(word, ph_sequence))

with open("long/{}/dict_long.txt".format(subword),"w+") as sout:
	sout.write("SENT-END\t\t\tsil\nSENT-START\t\t\tsil\n")
	for word,ph_sequence in dict_small_long_list:
		sout.write("{}\t\t\t{}\n".format(word, ph_sequence))
