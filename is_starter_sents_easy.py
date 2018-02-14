from client_util import is_easy

with open('starter_sents.txt','r') as fin:
	lines = fin.read().split('\n')
	sents_in = []
	levels_in = []
	for line in lines:
		s,l = line.split('\t')
		sents_in.append(s)
		levels_in.append(l)

res = {0:[],1:[],2:[]}
for lvl in range(3):
	for s in sents_in:
		if is_easy(s,lvl):
			res[lvl].append(s)

lvl3 = list(set(res[2]) - set(res[1]).union(set(res[0])) )
lvl2 = list(set(res[1]) - set(res[0]))
lvl1 = list(set(res[0]))

with open('starter_sents_level_by_kt_words_leeway.txt','w') as fout:
	for lvl_idx, g in enumerate([lvl1,lvl2,lvl3]):
		for s in g:
			lout = '%d\t%d\t%s\n'%(len(s.split()),lvl_idx+1,s)
			fout.write(lout)
		