class Phoneme(object):
	def __init__(self, ipa, ortho):
		self.ipa = ipa
		self.ortho = ortho
		self.sonority = -1
	
	def __unicode__(self):
		return self.ipa
	
	def __str__(self):
		return self.ortho
	
	def __eq__(self, other):
		if isinstance(other, (unicode, str)):
			return other == self.ortho
		elif isinstance(other, Phoneme):
			return other.ortho == self.ortho
		return False
	
	def __ne__(self, other):
		return not (self == other)

class Frontness(object):
	FRONT = 1
	CENTER = 2
	BACK = 3

class Height(object):
	HIGH = 1
	MID = 2
	LOW = 3

class Vowel(Phoneme):
	def __init__(self, ipa, ortho, frontness, height, rounded, nasalized):
		super(Vowel, self).__init__(ipa, ortho)
		self.frontness = frontness
		self.height = height
		self.rounded = rounded
		self.nasalized = nasalized
		self.sonority = 99

class Position(object):
	BILABIAL = 1
	LABIODENTAL = 2
	ALVEOLAR = 3
	POSTALVEOLAR = 4
	PALATAL = 5
	VELAR = 6
	UVULAR = 7
	GLOTTAL = 8
	EPIGLOTTAL = 9

class Articulation(object):
	APPROX = 1
	LATERAL = 2
	NASAL = 3
	FRICATIVE = 4
	PLOSIVE = 5

class Consonant(Phoneme):
	def __init__(self, ipa, ortho, position, articulation, voiced):
		super(Consonant, self).__init__(ipa, ortho)
		self.position = position
		self.articulation = articulation
		self.voiced = voiced
		self.sonority = articulation

PHONEMES = (
	Vowel(u'i', 'i', Frontness.FRONT, Height.HIGH, False, False),
	Vowel(u'u', 'u', Frontness.BACK, Height.HIGH, True, False),
	Vowel(u'\u025C', 'e', Frontness.FRONT, Height.MID, False, False),
	Vowel(u'\u0254', 'o', Frontness.BACK, Height.MID, True, False),
	Vowel(u'a', 'a', Frontness.FRONT, Height.LOW, False, False),
	Consonant(u'm', 'm', Position.BILABIAL, Articulation.NASAL, True),
	Consonant(u'p', 'p', Position.BILABIAL, Articulation.PLOSIVE, False),
	Consonant(u'b', 'b', Position.BILABIAL, Articulation.PLOSIVE, True),
	Consonant(u'f', 'f', Position.LABIODENTAL, Articulation.FRICATIVE, False),
	Consonant(u'v', 'v', Position.LABIODENTAL, Articulation.FRICATIVE, True),
	Consonant(u'n', 'n', Position.ALVEOLAR, Articulation.NASAL, True),
	Consonant(u't', 't', Position.ALVEOLAR, Articulation.PLOSIVE, False),
	Consonant(u'd', 'd', Position.ALVEOLAR, Articulation.PLOSIVE, True),
	Consonant(u's', 's', Position.ALVEOLAR, Articulation.FRICATIVE, False),
	Consonant(u'z', 'z', Position.ALVEOLAR, Articulation.FRICATIVE, True),
	Consonant(u'r', 'r', Position.ALVEOLAR, Articulation.APPROX, True),
	Consonant(u'l', 'l', Position.ALVEOLAR, Articulation.LATERAL, True),
	Consonant(u'\u0283', 'sh', Position.POSTALVEOLAR, Articulation.FRICATIVE, False),
	Consonant(u'\u0292', 'zh', Position.POSTALVEOLAR, Articulation.FRICATIVE, True),
	Consonant(u'\u014B', 'ng', Position.VELAR, Articulation.NASAL, True),
	Consonant(u'j', 'j', Position.PALATAL, Articulation.APPROX, True),
	Consonant(u'k', 'k', Position.VELAR, Articulation.PLOSIVE, False),
	Consonant(u'g', 'g', Position.VELAR, Articulation.PLOSIVE, True),
	Consonant(u'x', 'kh', Position.VELAR, Articulation.FRICATIVE, False),
	Consonant(u'\u0263', 'gh', Position.VELAR, Articulation.FRICATIVE, True),
	Consonant(u'q', 'q', Position.UVULAR, Articulation.PLOSIVE, False),
	Consonant(u'\u03C7', 'qh', Position.UVULAR, Articulation.FRICATIVE, False),
	Consonant(u'\u0294', '\'', Position.GLOTTAL, Articulation.PLOSIVE, False),
	Consonant(u'h', 'h', Position.GLOTTAL, Articulation.FRICATIVE, False),
)

def phoneme(str):
	for ph in PHONEMES:
		if ph.ortho == str:
			return ph
	raise ValueError("'{}' is not a valid phoneme".format(str))
