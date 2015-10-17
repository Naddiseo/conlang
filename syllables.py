# -*- coding: utf-8 -*-
from __future__ import division
import codecs, sys
from itertools import combinations_with_replacement, chain, permutations
from phonics import PHONEMES, phoneme as p, \
	Vowel, Consonant, Articulation as A, Position

art_pn = [A.PLOSIVE, A.NASAL]
art_al = [A.APPROX, A.LATERAL]
art_fp = [A.FRICATIVE, A.PLOSIVE]

def valid_codas(c):
	l = len(c)
	# /j/ not allowed in coda
	return c[0] != 'j' if l == 1 else (l == 0)
	
#import pdb;pdb.set_trace()
assert not valid_codas([p('k'), p('kh')])
assert not valid_codas([p('b'), p('v')])
assert not valid_codas([p('j')])

def valid_onsets(c):
	c1 = c2 = c3 = None
	l = len(c)
	
	if l == 0:
		return True
	
	if l > 1:
		# /ʔ/ not allowed in onset
		# 9. Velar, uvular, and glottal fricatives cannot appear in clusters
		for phone in ('\'', 'kh', 'gh', 'qh', 'h'):
			if phone in c:
				return False
	
	
	if l == 1:
		c1 = c[0]
	elif l == 2:
		c1, c2 = c
		
		if c1 == 's' and c2 == 't':
			print("HELLO WORLD")
		
		if c2 == 'j':
			# /j/ only allowed in onset matching Cj where C is plosive or fricative more forward than palatal
			if c1.articulation in (A.PLOSIVE, A.FRICATIVE) and c1.position < Position.PALATAL:
				return True
			else:
				return False
		
		# 2. CC must agree in voicing
		if c1.voiced != c2.voiced:
			return False
		
		# 3. [+plosive][+nasal] cluster is disallowed
		if c1.articulation == A.PLOSIVE and c2.articulation == A.NASAL:
			return False
		# 4. [+nasal][+plosive] cluster is disallowed
		if c1.articulation == A.NASAL and c2.articulation == A.PLOSIVE:
			return False
		
		# 5. No geminates
		if c1 == c2:
			return False
		
		# 7. NN cluster not allowed
		if c1.articulation == A.NASAL and c2.articulation == A.NASAL:
			return False
		
		# 8. /r/ + nasal cluster not allowed
		if c1 == 'r' and c2.articulation == A.NASAL:
			return False
		
		# 10. NC is not allowed (except Nj)
		if c1.articulation == A.NASAL and c2 != 'j':
			return False
		
		# 11. [+alveolar] + /l/ is not allowed
		if c1.position == Position.ALVEOLAR and c2 == 'l':
			return False
		
		# 12. CC is not allowed where position is velar, uvular, or glottal
		if c1.position > Position.PALATAL and c2.position > Position.PALATAL:
			return False
		
		# 13. Cluster cannot start with with lateral or approximate
		if c1 in ('j', 'l', 'r'):
			return False
		
		# 14. [+alveolar, +plosive][+labial, +plosive] not allowed
		if c1.position == Position.ALVEOLAR and c2.position == Position.BILABIAL:
			if c1.articulation == A.PLOSIVE and c2.articulation == A.PLOSIVE:
				return False
		
	elif l == 3:
		c1, c2, c3 = c
		
		# /j/ not allowed in 3 consonant cluster
		if 'j' in c:
			return False
		
		# 2. CC must agree in voicing
		if c1.voiced != c2.voiced or c2.voiced != c3.voiced:
			return False
		
		# 3. [+plosive][+nasal] cluster is disallowed
		if c1.articulation == A.PLOSIVE and c2.articulation == A.NASAL:
			return False
		# 4. [+nasal][+plosive] cluster is disallowed
		if c1.articulation == A.NASAL and c2.articulation == A.PLOSIVE:
			return False
		# 3. [+plosive][+nasal] cluster is disallowed
		if c2.articulation == A.PLOSIVE and c3.articulation == A.NASAL:
			return False
		# 4. [+nasal][+plosive] cluster is disallowed
		if c2.articulation == A.NASAL and c3.articulation == A.PLOSIVE:
			return False
		
		# 5. No geminates
		if c1 == c2 or c2 == c3:
			return False
		
		# 6. CCC cannot have the same manner 
		if c1.articulation == c2.articulation and c2.articulation == c3.articulation:
			return False
		
		# 7. NN cluster not allowed
		if c1.articulation == A.NASAL and c2.articulation == A.NASAL:
			return False
		if c2.articulation == A.NASAL and c3.articulation == A.NASAL:
			return False
		
		# 8. /r/ + nasal cluster not allowed
		if c2 == 'r' and c3.articulation == A.NASAL:
			return False
		
		# 10. NC is not allowed (except Nj)
		if c1.articulation == A.NASAL and c2 != 'j':
			return False
		if c2.articulation == A.NASAL and c3 != 'j':
			return False
		
		# 11. [+alveolar] + /l/ is not allowed
		if c1.position == Position.ALVEOLAR and c2 == 'l':
			return False
		if c2.position == Position.ALVEOLAR and c3 == 'l':
			return False
		
		# 12. CC is not allowed where position is velar, uvular, or glottal
		if c1.position > Position.PALATAL and c2.position > Position.PALATAL:
			return False
		if c2.position > Position.PALATAL and c3.position > Position.PALATAL:
			return False
		
		# 13. Cluster cannot start with with lateral or approximate
		if c1 in ('j', 'l', 'r'):
			return False
		
		# 14. [+alveolar, +plosive][+labial, +plosive] not allowed
		if c1.position == Position.ALVEOLAR and c2.position == Position.BILABIAL:
			if c1.articulation == A.PLOSIVE and c2.articulation == A.PLOSIVE:
				return False
		if c2.position == Position.ALVEOLAR and c3.position == Position.BILABIAL:
			if c2.articulation == A.PLOSIVE and c3.articulation == A.PLOSIVE:
				return False
		
	else:
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
	permutations(C, 1),
	permutations(C, 2),
	permutations(C, 3),
	combinations_with_replacement(C, 2),
	combinations_with_replacement(C, 3),
)

nuclei = [[ph] for ph in V] + DIPH
codas = list(combinations_with_replacement(C, 1)) + [[]]
onsets = list(CLUSTERS) + [[]]
codas = filter(valid_codas, codas)
onsets = filter(valid_onsets, onsets)

print len(onsets), len(nuclei), len(codas)
print '=', len(nuclei) * len(codas) * len(onsets)

syllables = set()
o = len(onsets) + len(nuclei)
t = o
i = 0
for onset in onsets:
	syllables.update([u'{}\n'.format(u''.join(o.ipa for o in onset))])
	continue
	for nucleus in nuclei:
		sys.stderr.write('{:.2f}\r'.format(i / t * 100))
		i += 1
		for coda in codas:
			syllables.update([u'{}{}{}\n'.format(
				u''.join(o.ipa for o in onset),
				u''.join(n.ipa for n in nucleus),
				u''.join(c.ipa for c in coda)
			)])
		t = o + len(syllables)

with codecs.open('syls.txt', 'w', encoding = 'utf-8') as f:	
	syllables = sorted(syllables)
	syllables = sorted(syllables, key = len)
	for syllable in syllables:
		sys.stderr.write('{:.2f}\r'.format(i / t * 100))
		i += 1
		f.write(syllable)
