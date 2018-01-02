"""
Open monophones0 and proto.
For every line in hmmdefs, prepend ~h
Then quote the actual phone 
Write this to the file hmmdefs
"""

fin = open('monophones0','r')
fp = open('proto','r')

proto = fp.readlines()[4:]

lines = []
for ph in fin.readlines():
	ph = ph.strip('\n')
	lines.append("~h \"{}\"\n".format(ph))
	lines.extend(proto)

fout = open('hmmdefs','w+')
for l in lines:
	fout.write(l)
