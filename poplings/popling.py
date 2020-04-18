import random
import math
import DNA
import food
import network

class Popling:
    def __init__(self, pos=None, parent=None):
        if pos == None:
            self.x = random.randrange(0,500)
            self.y = random.randrange(0,500)
        else:
            self.x = pos[0]
            self.y = pos[1]
        if parent == None:
            self.dna = DNA.Genes()
            self.radius = random.randrange(5, 40)
            self.generation = 1

        else:
            self.dna = DNA.Genes(parent)
            self.radius = parent.radius
            self.generation = parent.generation + 1

        self.maxHealth = self.dna.healthFactor * self.radius
        self.health = self.maxHealth
        self.velocity = self.dna.speedFactor/self.radius
        self.direction = 30
        self.bounds = [500,500]
        self.seekingFood = None

    def dist(self, x, y):
        fx = (self.x-x)**2
        fy = (self.y-y)**2
        d = (fx+fy)**(1/2)
        return d


    def decision(self, foodBlock):
        d = self.dna.nn.output(self.health, self.maxHealth)
        if d[0] > 0.3:
            self._seek(foodBlock)
        else:
            self.seekingFood = None

    def _seek(self, foodBlock):
        if len(foodBlock) > 0 and self.seekingFood == None:
            closest = foodBlock[0]
            d = self.dist(closest.x, closest.y)
            for f in foodBlock:
                d2 = self.dist( f.x, f.y)
                if  d2 < d:
                    d = d2
                    closest = f
            self.seekingFood = closest
            # print(self.x, self.y ,closest.x, closest.y, d, end = " ")
            upper = closest.y - self.y
            lower = closest.x - self.x
            if lower == 0:
                lower = 0.000000000000000001
            angle = math.degrees(math.atan(upper/lower))
            # print("angle=" + str(angle))
            self.direction = angle
            

    def move(self, foodBlock, poplings):

        # changing direction
        ch = random.randrange(1,100)
        if ch>98 and self.seekingFood == None:
            angle = random.randrange(int(self.direction - 10) , int(self.direction + 10))
            if angle<0:
                angle = 360 - angle
            self.direction += angle
            self.direction %= 360
        
        #seeking food #alpha stage
        # doing unexected shimmering around the food

        self.decision(foodBlock)

        #moving
        self.x += int(self.velocity * math.cos(self.direction))
        self.y += int(self.velocity * math.sin(self.direction))

        #correcting boundaries
        if self.x<0 or self.x > self.bounds[0]:
            self.x -= int(self.velocity * math.cos(self.direction))
        if self.y<0 or self.y > self.bounds[1]:
            self.y -= int(self.velocity * math.sin(self.direction))

        #checking collision with food
        for f in foodBlock:
            if self.dist(f.x, f.y) <= f.radius + self.radius:
                if f.type == "Non-Veg":
                    if self.dna.eatingHabit == "Non-Veg":
                        self.health += f.regeneration
                        if self.health > self.maxHealth:
                            self.health = self.maxHealth
                            foodBlock.remove(f)
                else:
                    self.health += f.regeneration
                    if self.health>self.maxHealth:
                        self.health = self.maxHealth
                    foodBlock.remove(f)


    def reproduce(self):
        pop = Popling(pos=[self.x, self.y], parent=self)
        return pop

    def die(self, foodBlock):
        f_count = random.randrange(3,5)
        left = self.x - self.radius
        up = self.y - self.radius
        right = self.x + self.radius
        down = self.y + self.radius

        if self.radius < 6:
            f_count = 1

        for _ in range (1, f_count+1):
            f = food.Food([right,down], [left, up], r=int(self.radius/f_count))
            f.type = "Non-Veg"
            f.regeneration *= 2
            foodBlock.append(f)






