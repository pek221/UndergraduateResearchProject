import random
import math
from Parameters import Parameters

class Person:

    # Initializes the person with thei condition, location, and moving variable
    def __init__(self,i,x,y,S,I):
        self.ID = i
        self.Susceptible = S
        self.Infective = [I,0]
        self.Recovered = False
        self.Dead = False
        self.location = (x, y)
        self.quadrant = (self.location[0]%10, self.location[1]%10)
        list = []
        for i in range(30):
            list.append(random.randint(10, 50))
            list.append(random.randint(-50, -10))
        self.moveX = random.choice(list)
        self.moveY = random.choice(list)
        self.parameters = Parameters()

    # Moves the person according to their random moving variable and ensures that people stay within the town boundaries
    def move(self,size):
        xmax, ymax, xmin, ymin = size[0], size[1], 10, 10
        x, y = self.location[0], self.location[1]
        if x <= xmin:
            self.moveX = random.randint(10,50)
        elif x >= xmax:
            self.moveX = random.randint(-50,-10)
        if y <= ymin:
            self.moveY = random.randint(10,50)
        elif y >= ymax:
            self.moveY = random.randint(-50,-10)
        self.location = (x+self.moveX, y+self.moveY)
        self.quadrant = (self.location[0]%10, self.location[1]%10)
        if self.Infective[0]:
            self.check_recovery()

    # Increments the invective person's recovery by 1 hr until 2 weeks is reached, and the person becomes either recovered or dead
    def check_recovery(self):
        if self.Infective[1] < 730:
            self.Infective[1] += 1
            return
        if self.Infective[1] >= 336:
            self.Infective = [False,0]
            dead = int(self.parameters.deathRate*100)
            recovered = 100 - dead
            my_list = ['D']*dead + ['R']*recovered
            condition = random.choice(my_list)
            if condition == 'D':
                self.Dead = True
            elif condition == 'R':
                self.Recovered = True
        return

    # Finds the susceptible neighbors of a given person
    def find_neighbors(self, population):
        neighbors = []
        # If the a person in not susceptible or not in a nearby quadrant, they are skipped. Otherwise, the distance is calculated and if it is less than the infection radius, they are a valid neigbor.
        for person in population:
            if not person.Susceptible:
                continue
            if abs(self.quadrant[0] - person.quadrant[0]) > 2 or abs(self.quadrant[1] - person.quadrant[1]) > 2:
                continue
            distance = self.find_distance(person)
            if 1 < distance < self.parameters.infectionRadius*100:
                neighbors.append(person)
        return neighbors

    # For each neighbor, there is a certain likelihood that they become infected (the infection rate). If they are infected, they ar eno longer susceptible
    def try_to_infect_neighbors(self, neighbors, infectionRate):
        for neighbor in neighbors:
            if neighbor.Susceptible == True:
                infective = int(infectionRate * 100)
                susceptible = 100 - infective
                my_list = ['I'] * infective + ['S'] * susceptible
                condition = random.choice(my_list)
                if condition == 'I':
                    neighbor.Susceptible = False
                    neighbor.Infective[0] = True

    # Caluclates the distance between two people
    def find_distance(self, person):
        x1,y1 = self.location[0], self.location[1]
        x2,y2 = person.location[0], person.location[1]
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance