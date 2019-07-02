class Color:

	@staticmethod
	def get(a, b, c, d):
		return (Color.clr(d) << 24) + (Color.clr(c) << 16) + (Color.clr(b) << 8) + (Color.clr(a))

	@staticmethod
	def clr(d):
		if d < 0: return 255
		r = int(d / 100 % 10)
		g = int(d / 10 % 10)
		b = int(d % 10)
		return r * 36 + g * 6 + b