from random import choice
import codecs

VALUES = { d:[] for d in xrange(10) }

with codecs.open('difficulty.tsv', 'r', encoding='utf-8') as fp:
	fp.readline()
	for line in fp:
		pair, hardness = line.strip().split('\t')
		
		VALUES[int(hardness)].append(pair)
		
		
print u'{}'.format(choice(VALUES[0]))


