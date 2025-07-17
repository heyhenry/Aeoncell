class MrRoboto:
    def __init__(self,
                    height: int = 100,
                    weight: int = 1000,
                    colour: str = "White"):
        self.height = height
        self.weight = weight
        self.colour = colour

    def print_colour(self):
        print(self.colour)

test = MrRoboto()
test.print_colour()

og_init = MrRoboto.__init__
def updated_colour(self, *args, **kwargs):
    og_init(self, *args, **kwargs)
    self.colour = "Blue"

MrRoboto.__init__ = updated_colour

new_test = MrRoboto()
new_test.print_colour()