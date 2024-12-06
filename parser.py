
def decode_string(indata):
	num = ''
	active = True
	out = ''
	for x in indata:
		if active:
			if x == '>':
				if num: 
					outchar = int(num)
					out += chr(outchar)
				num = ''
				active = False
			else:
				num += x
		else:
			if x == '<':
				active = True
			else:
				out += x
	return out

class mc_track_placement:
	def __init__(self, indata):
		self.pos = 0
		self.tracknum = 0
		self.sectionnum = 0
		self.repeats = 0
		self.startat = 1
		self.transpose = 0
		self.instnum = 0
		if indata: self.read(indata)

	def read(self, indata):
		if indata:
			if indata[0]:
				for n, x in enumerate(indata):
					if n == 0: self.pos = float(x)
					if n == 1: self.tracknum = float(x)
					if n == 2: self.sectionnum = int(x)
					if n == 3: self.repeats = float(x)
					if n == 4: self.startat = float(x)
					if n == 5: self.transpose = int(x)
					if n == 6: self.instnum = int(x)

class mc_instrument:
	def __init__(self, indata):
		self.name = ''
		self.midi_patch = 0
		self.midi_bank = 0
		self.unk1 = 0
		self.params = []
		if indata: self.read(indata)

	def read(self, indata):
		for n, x in enumerate(indata):
			if n == 0: self.name = decode_string(x)
			if n == 1: self.midi_patch = int(x)
			if n == 2: self.midi_bank = int(x)
			if n == 4: 
				if x:
					if x[0] == 'v':
						self.params = [int(x) for x in x[1:].split('=')]

class mc_soundfont:
	def __init__(self, indata):
		self.name = ''
		self.path = ''
		if indata: self.read(indata)

	def read(self, indata):
		for n, x in enumerate(indata):
			if n == 0: self.name = decode_string(x)
			if n == 1: self.path = decode_string(x)

class mc_section:
	def __init__(self, indata):
		self.name = ''
		self.unk1 = ''
		self.unk2 = ''
		self.notes = ''
		self.unk4 = ''
		self.color = ''
		self.unk6 = ''
		self.unk7 = []
		self.unk8 = ''
		if indata: self.read(indata)

	def read(self, indata):
		for n, x in enumerate(indata):
			if n == 0: self.name = decode_string(x)
			if n == 1: self.unk1 = x
			if n == 2: self.unk2 = x
			if n == 3: self.notes = x
			if n == 4: self.unk4 = x
			if n == 5: self.color = x
			if n == 6: self.unk6 = x
			if n == 7: 
				self.auto = mc_sectionauto(x.split('='))
				#self.auto = [[x.split('#') for x in x.split('!')] for y in c]
			if n == 8: self.unk8 = x
		print(self.unk4, self.color, self.unk6)

class mc_sectionauto:
	def __init__(self, indata):
		self.points = []
		if indata: self.read(indata)

	def read(self, indata):
		for x in indata:
			self.points.append( [x.split('#') for x in x.split('!')] )

class mc_general:
	def __init__(self, indata):
		self.tempo = 120
		self.trackvol = []
		self.tracknames = []
		if indata: self.read(indata)

	def read(self, indata):

		for n, x in enumerate(indata):
			if x:
				if n == 1: self.tempo = int(x[0])
				if n == 2: self.trackvol = [int(y) for y in x]
				if n == 9: self.tracknames = [decode_string(y) for y in x]

class mc_song:
	def __init__(self):
		self.general = mc_general(None)
		self.section = None
		self.track = None
		self.instrument = None
		self.drum_kit = None
		self.sound_font = None
		self.section_order = None

	def load_from_file(self, input_file):
		song_file = open(input_file, 'r')

		splitteddata = song_file.read().split('/')
		for n, d in enumerate(splitteddata):
			if n == 0: self.general.read([x.split(',') for x in d.split(';')])
			if n == 1: self.section = [mc_section(x.split(',')) for x in d.split(';')]
			if n == 2: self.track = [mc_track_placement(x.split(',')) for x in d.split(';')]
			if n == 3: self.instrument = [mc_instrument(x.split(',')) for x in d.split(';')]
			if n == 4: self.drum_kit = [mc_instrument(x.split(',')) for x in d.split(';')]
			if n == 5: self.sound_font = [mc_soundfont(x.split(',')) for x in d.split(';')]
			if n == 6: self.section_order = [x.split(',') for x in d.split(';')]


testin = mc_song()
testin.load_from_file("C:\\Program Files (x86)\\MuMuNebula\\emulator\\nebula\\nebula\\fs_dynamic\\data\\data\\com.musicmaker.mobile.android\\files\\projects\\vn92aN4tsUENzZzN")
