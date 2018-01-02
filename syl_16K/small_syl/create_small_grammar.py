"""
https://stackoverflow.com/questions/15719817/htk-hvite-cant-find-hmm

Create File of form :
$digit = ONE | TWO | THREE | FOUR | FIVE | SIX | SEVEN | EIGHT | NINE | OH | ZERO;

( SENT-START DIAL <$digit> SENT-END )


Input file : wlist
Output file : grammar
"""
folder = 'short'
subword = 'mono' #Change to mono | tri | syl


with open('{}/{}/wlist_{}.txt'.format(folder, subword, folder),'r') as win:
	wlist = win.readlines()[2:]

word_str = ''
for line in wlist:
	word = line.strip()
	word_str = word_str + word
	if line != wlist[-1]:
		word_str = word_str + " | "

word_str = word_str + ";"

with open('{}/{}/grammar_{}'.format(folder, subword, folder),'w+') as gout:
	gout.write('$word = ')
	gout.write(word_str)
	gout.write('\n\n( SENT-START $word SENT-END )')


