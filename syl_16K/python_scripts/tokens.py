
def read_token_files():
	"""Categorize and Generate list of tokens.

	Tokens are categorized into 4 types: Vowels, Consonants, Alankars(Diacritics), & Yogavahas. The last type only has 2 constitutents, so they are not stored a separate file. The former 3 files however, have tokens listed on every line. This method extracts tokens into lists.

	Returns:
		tuple: 
			vowels (list): Vowels of the language.
			consonants (list): Consonants of the language.
			alankars (list): list of tuples in the with the following fields.
				Diacritic (string): also called `alankars`.
				Corrusponding Vowel (string)

	"""
	#Get alankaras
	alankars = []
	with open('tokens/alankaras.txt','r') as af:
		for line in af.readlines():
			line = line.strip('\n\r')
			ala, let = line.split(' ')
			alankars.append( (ala, let) )

	#Get vowels
	vowels = []
	with open('tokens/vowels.txt','r') as vf:
		for line in vf.readlines():
			let = line.strip('\n\r')
			vowels.append(let)

	#Get consonants
	consonants = []
	with open('tokens/consonants.txt','r') as vf:
		for line in vf.readlines():
			let = line.strip('\n\r')
			consonants.append(let)

	return (vowels, consonants, alankars)

def get_tokens(subword):
	""" Perform Kannada Tokenization 

	Hexadecimal Encoding list a of Kannada word is grouped in sets of 3. Each corresponds to a unique Token of the language.

	Args:
		subword(str) : A Kannada word input
	Returns:
		list of tokens for `subword`.

	"""
	parts = list(subword)
	return [unicode(i+j+k, 'utf-8').encode('utf-8') for i,j,k in zip(parts[::3], parts[1::3],parts[2::3])]


def get_monophones(tokens, vowels, consonants, alankars):
	"""Finds the constitutent monophones of an input subword.

	Args:
		tokens (list) : Kannada list of elements in a subword unit.
	Returns:
		phonemes (list) : list of constitutent monophones.

	"""
	phonemes = []
	#Convert to phonemes
	for token in tokens:		
		if token == 'ಂ' : phonemes.append('ಮ್')
		if token == 'ಃ': phonemes.extend(['ಹ್','ಅ'])

		#if token between ಅ to ಔ, append to list 
		if token in vowels:
			phonemes.append(token)
			continue

		#if token between ಕ and ಹ, concatenate ್ and push ಅ
		if token in consonants:
			phonemes.append(token+'್')
			phonemes.append('ಅ')
			continue

		#if token between , pop (ಅ) and add the corrusponding vowel from ಆ to ಔ
		tup = [y for x,y in alankars if x==token]
		if tup:
			del phonemes[-1]
			phonemes.append(tup[0])
			continue

		#if ್, pop last item (ಅ) from list and continue. 
		if token == '್':
			del phonemes[-1]


	return phonemes

def get_syllables(tokens, vowels, consonants, alankars):
	""" Constructs constitutent syllables of list of tokens of a word.

	Algorithm:
		Iterate though the list of tokens and for every token category encountered, follow the corresponding step:
			If vowel : 
				Every vowel is the beginning of a new syllable 
				- append to list

			If consonant : 
				Every consonant is the beginning of a new syllable
				- append to list

			If alankar : 
				Every alankar is a part of the previous syllable 
				- remove last element
				- attach alankar to element
				- put it back to the end of list

			if ್ : 
				್ and o are the end of a syllable
				- remove last element 
				- attach ್
				- push back to list

	Args: 
		tokens (list) : tokens of a word.
		vowels (list) : list 

	Returns:
		syllables (list) : list of constructed syllables of the list of tokens.

	"""
	syllables = []
	for token in tokens:

		#if token between ಅ to ಔ, append to list 
		if token in vowels:
			syllables.append(token)
			continue

		if token in consonants:
			syllables.append(token)
			continue

		#if token is alankars, pop last element, add the alankar to it, push it back
		if token in [x for x, y in alankars]:
			syl = syllables[-1]
			del syllables[-1]
			syllables.append(syl+token)
			continue

		if token in ['್', 'ಂ']:
			syl = syllables[-1]
			del syllables[-1]
			syllables.append(syl+token)
			continue

	return syllables


def get_triphones(word, mono):
	"""Creates triphones for the given word and monophone sequence.

	Args : 
		word (str) : Input word for which triphones for every syllable are required. (not used in function)
		mono (list) : List of monophones for the given word

	Returns :
		tri (list) : list of triphones for the input word

	"""
	tri = []
	if len(mono) == 1: 
		return [mono[0]]

	tri.append( mono[0]+"+"+mono[1])

	for i in range(2,len(mono)):
		tri.append(mono[i-2]+"-"+mono[i-1]+"+"+mono[i])

	tri.append(mono[len(mono)-2]+"-"+mono[len(mono)-1] )

	return tri

def get_syllables_all_words():
	"""Reads dict_syl.txt which consists of Syllables for every dictionary word.

	Returns:  
		syl_dict (tuple) : The list of tuples (word, syl)

	"""
	syl_dict = []
	with open('dict_syl.txt','r') as d:
		 for line in d.readlines():
		 	line = line.strip()
		 	word , _ , syl =  line.split('\t\t\t')
		 	syl = syl.split(' ')
		 	syl = syl[:-1] #Get rid of sp
		 	syl_dict.append( (word, syl) )

	return syl_dict