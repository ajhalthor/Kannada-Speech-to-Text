"""
Since HTK can better work with it's internal type, we convert wav files to MFCC feature vectors. 
This program creates a file "codetrain.scp" with the list of training audio files on the left and corrusponding 
output files on the right. 

"""
import random 

fout = open('codetrain.scp','w+')
fin = open('prompts.txt','r')

for line in fin.readlines():
	sample = line.split(' ')[0][2:]
	path = "samples_converted/{}.wav train/mfcc/{}.mfc\n".format(sample,sample)
	fout.write(path)

