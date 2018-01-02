"""
List path to training files in `train.scp`. This is created by takeing the right 
coulumn of paths in `codetrain.scp`. 
"""
lines = []
with open('codetrain.scp','r') as fin:
	lines = fin.readlines()

with open('train.scp','w+') as fout:
	for line in lines:
		line = line.strip('\n')
		path = line.split(' ')[1]
		fout.write("{}\n".format(path))
