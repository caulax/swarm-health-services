class Service:
	def __init__(self, name=None, image=None, new_image=None, status=None):
		self.name = name
		self.image = image
		self.new_image = new_image
		self.status = status

	def set_image(self, image):
		self.image = image

	def set_new_image(self, image):
		self.new_image = image
