"""
Since this problem is that of isolated word recognition, our grammar assumes the following form.
	Pause WORD Pause.

Example:
	The only variable term is the word to be recgonized. We thus create a Grammar file of the following form.
	$word = word1 | word2 | word3 | word4 | ... | wordN ;
	( SENT-START DIAL <$word> SENT-END )

Input: 
	List of words `wlist`.
Output: 
	Grammar of file `grammar`.

"""

with open('wlist','r') as win:
	wlist = win.readlines()[2:]

word_str = ''
for line in wlist:
	word = line.strip()
	word_str = word_str + word
	if line != wlist[-1]:
		word_str = word_str + " | "

word_str = word_str + ";"
#print word_str

with open('grammar','w+') as gout:
	gout.write('$word = ')
	gout.write(word_str)
	gout.write('\n\n( SENT-START $word SENT-END )')
