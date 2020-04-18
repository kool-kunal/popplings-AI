
import random

class Food:
    def __init__(self, boundsr, boundsl=None, r=None):
        if boundsl == None:
            boundsl = [0,0]
        self.x = random.randrange(boundsl[0],boundsr[0])
        self.y = random.randrange(boundsl[1],boundsr[1])
        if r == None:
            self.radius = random.randrange(10,20)
        else:
            self.radius = r
        self.regeneration = 5 * self.radius
        self.type = "Veg"

    