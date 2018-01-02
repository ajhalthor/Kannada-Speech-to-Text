"""
For every line in hmmdefs, prepend ~h and quote the actual phone. We then add contents of the `proto` after every phone.
This `proto` represents the initial state of all phones.
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
