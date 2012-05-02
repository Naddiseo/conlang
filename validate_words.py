import codecs, sys
from phonics import phoneme

words = []

with codecs.open('words.txt', 'r', encoding='utf-8') as fp:
	line_no = 0
	for line in fp:
		line = line.strip()
		
		sys.stderr.write('{:.2f} {}\r'.format(line_no/1600*100, line_no))
		line_no += 1
		
		word = u''
		
		i = 0
		l = len(line)
		while i < l:
			c = line[i]
			
			if c in u'szqgq' and i < l-1:
				c2 = line[i+1]
				if c2 == u'h':
					word += unicode(phoneme(u'{}{}'.format(c,c2)))
					i += 2
					continue
					
			elif c == u'n' and i < l-1:
				c2 = line[i+1]
				if c2 == u'g':
					word += unicode(phoneme(u'ng'))
					i += 2
					continue
			
			word += unicode(phoneme(c))
			i += 1
		
		words.append((line, word))

def is_valid(word):
	ortho, ipa = word
	# TODO: check if it's pronounceable 
	return False

for ortho, ipa in filter(is_valid, words):
	print ortho, ipa			
		
