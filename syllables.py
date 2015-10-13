from __future__ import division
import codecs,sys
from itertools import combinations, chain, permutations
from phonics import PHONEMES, phoneme as p, \
	Vowel, Consonant, Articulation as A, Position

art_pn = [A.PLOSIVE, A.NASAL]
art_al = [A.APPROX, A.LATERAL]
art_fp = [A.FRICATIVE, A.PLOSIVE]

def valid_cluster(c):
	l = len(c)
	
	if l < 2: return True
	if l > 3: return False
	
	pairs = [(c[0], c[1])]
	adj_pairs = [pairs[0]]
	
	if l == 3:
		pairs += [(c[1], c[2]), (c[0], c[2])]
		adj_pairs += [pairs[1]]
	
	for (c1, c2) in pairs:
		if c1 == c2:
			return False
		if c1.articulation == c2.articulation:
			if c1.articulation in art_pn:
				return False
			if c1.voiced is not c2.voiced:
				return False
		if c1.articulation in art_al and c2.articulation in art_al:
			return False
			
		if c1.articulation == A.NASAL and c2.articulation in art_al:
			# nl / ngl / nr / mr
			return False
	
	for (c1, c2) in adj_pairs:
		if c1.voiced is not c2.voiced:
			if c1.articulation in art_fp and c2.articulation in art_fp:
				return False
		if c1.articulation == A.NASAL and c2.articulation == A.FRICATIVE:
			return False
		if c1.articulation == A.FRICATIVE \
			and c1.position == Position.ALVEOLAR \
			and	c2.position == Position.UVULAR:
			return False
		if c1.position > Position.ALVEOLAR and c2.position > Position.ALVEOLAR:
			if c1.articulation == c2.articulation:
				return False
		
		if c1.articulation in art_al and c2.articulation == A.FRICATIVE:
			return False
	
	if l == 3:
		c1,c2,c3 = c
		
		if c2.articulation in art_pn:
			if c3.position >= c2.position: # (c)kx / (c)kqh / (c)nqg
				return False
	
	return True
	
def valid_codas(c):
	l = len(c)
	
	if l < 2: return True
	
	pairs = [(c[0], c[1])]
	adj_pairs = [pairs[0]]
	
	if l == 3:
		pairs += [(c[1], c[2]), (c[0], c[2])]
		adj_pairs += [pairs[1]]
	
	for pair in pairs:
		c1, c2 = pair
		
		if c1.articulation == A.PLOSIVE:
			if c2.articulation == A.NASAL:
				return False
		if c2.articulation in art_al: # No approx in syllable final
			return False
		
	return True
	
def valid_onsets(c):
	l = len(c)
	
	if l < 2: return True
	
	pairs = [(c[0], c[1])]
	adj_pairs = [pairs[0]]
	
	if l == 3:
		pairs += [(c[1], c[2]), (c[0], c[2])]
		adj_pairs += [pairs[1]]
	
	for pair in pairs:
		c1,c2 = pair
		if c1.articulation in art_al + [A.NASAL]: # approx in syllable initial
			if c2.articulation == A.PLOSIVE:
				return False
	
	return True

CONSONS = [ph for ph in PHONEMES if isinstance(ph, Consonant)]
GLOTTALS = [ph for ph in CONSONS if ph.position is Position.GLOTTAL]

V = [ph for ph in PHONEMES if isinstance(ph, Vowel)]
C = [ph for ph in CONSONS if ph.position is not Position.GLOTTAL]

i = p('i')
DIPH = [
	[p(letter), i] for letter in ('a', 'o', 'e')
] + [
	[i, p(letter)] for letter in ('a', 'o', 'e', 'u')
]

CLUSTERS = chain(
	combinations(C, 1),
	combinations(C, 2),
)

nuclei = [[ph] for ph in V] + DIPH
codas = filter(valid_cluster, CLUSTERS) + [[]]
onsets = codas + [[ph] for ph in GLOTTALS]

codas = filter(valid_codas, codas)
onsets = filter(valid_onsets, onsets)

print len(nuclei), len(codas), len(onsets)
print '=', len(nuclei) * len(codas) * len(onsets)

syllables = set()
o = len(onsets) +len(nuclei)
t = o
i = 0
for onset in onsets:
	for nucleus in nuclei:
		sys.stderr.write('{:.2f}\r'.format(i/t*100))
		i += 1
		for coda in codas:
			syllables.update([u'{}{}{}\n'.format(
				u''.join(o.ipa for o in onset), 
				u''.join(n.ipa for n in nucleus), 
				u''.join(c.ipa for c in coda)
			)])
		t = o+len(syllables)

with codecs.open('syls.txt', 'w', encoding = 'utf-8') as f:	
	syllables = sorted(syllables)
	syllables = sorted(syllables, key=len)
	for syllable in syllables:
		sys.stderr.write('{:.2f}\r'.format(i/t*100))
		i += 1
		f.write(syllable)
