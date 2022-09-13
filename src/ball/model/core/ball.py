class Ball:
    def __init__(self, name, mass, radius, cda):
        self.name = name
        self.mass = mass
        self.cda = cda
        self.radius = radius

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}>'
