import random
import network

class Genes:
    def __init__(self, parent = None):
        self.healthFactor = random.randrange(15, 25)
        self.speedFactor = random.randrange(80,120)
        self.eyes = random.randrange(1, 1000)
        self.color = (0, 0, 0)
        self.eatingHabit = "Veg"
        self.nn = network.net(2, 1)

        if parent != None:
            self.healthFactor = parent.dna.healthFactor
            self.speedFactor = parent.dna.speedFactor
            self.eyes = parent.dna.eyes
            self.color = parent.dna.color
            self.eatingHabit = parent.dna.eatingHabit
            self.nn = parent.dna.nn
            m = random.random()
            if m < 0.2:
                self._mutate(parent)


    def _mutate(self, parent):
        self.healthFactor = parent.dna.healthFactor*random.uniform(0.9, 1.2)
        self.speedFactor = parent.dna.speedFactor*random.uniform(0.5, 1.5)
        self.eyes = parent.dna.eyes*random.uniform(0.5,1.5)
        self.eatingHabit = random.choice(["Veg", "Non-Veg"])
        self.nn.mutate(0.2, 0.4)
        #colorchange
        red = parent.dna.color[0] + random.randrange(-50,50)
        if red<0 or red>255:
            red = parent.dna.color[0]
        green = parent.dna.color[1] + random.randrange(-50,50)
        if green<0 or green>255:
            green = parent.dna.color[1]
        blue = parent.dna.color[2] + random.randrange(-50,50)
        if blue<0 or blue>255:
            blue = parent.dna.color[2]
        self.color = (red, green, blue)
        print("----MUTATED----")
        print("parent INFO:")
        print("healthFactor=", parent.dna.healthFactor, "speedFactor=", parent.dna.speedFactor, "color=", parent.dna.color, "eyes=", parent.dna.eyes)
        print("child INFO:")
        print("healthFactor=", self.healthFactor, "speedFactor=", self.speedFactor, "color=", self.color, "eyes=", self.eyes)