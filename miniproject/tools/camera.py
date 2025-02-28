from tools.raycaster import RayCaster


class Camera:
    def __init__(self, character=None, world=None):
        self.x = 300
        self.y = 100
        self.z = 0

        self.angle = 0
        self.pitch = 0

        if character is None:
            self.raycaster = RayCaster(self, world)
        else:
            self.raycaster = RayCaster(character, world)

    def get_position(self):
        return self.x, self.y

    def update(self):
        self.raycaster.update()
