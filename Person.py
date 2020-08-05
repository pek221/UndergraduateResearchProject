import random
import math
from Parameters import Parameters

class Person:

    # Initializes the person with thei condition, location, and moving variable
    def __init__(self,i,x,y,S,I, house, store, friends):
        self.ID = i
        self.Susceptible = S
        self.Infective = [I,0]
        self.Recovered = False
        self.Dead = False
        self.location = (x, y)
        self.parameters = Parameters()
        self.home = house
        self.store = store
        self.friends = friends
        self.quadrant = (self.location[0]%10, self.location[1]%10)
        self.movement = [self.location,(0,0)]
        self.moveX, self.moveY = [0,0,0], [0,0,0] #[moving variable, amount of journey traveled, length of journey]
        self.initializeMotion()

    def initializeMotion(self):
        self.movement[0] = self.location
        if self.isHome():
            store = int(100*self.parameters.probGoShopping)
            stay = int(100*self.parameters.probStayHome)
            friend = int(100*self.parameters.probVisitFriend)
            list = store*['Store'] + stay*['Stay'] + friend*['Friend']
            movement = random.choice(list)
            if movement == 'Stay':
                self.movement[1] = self.location
                speed = random.choice([20, 30, 40, 50, 60, 70, 80])
                self.moveX = [0,0,speed]
                self.moveY = [0,0,speed]
                return
            if movement == 'Store':
                self.movement[1] = self.store.location
                speed = random.choice([20,30, 40, 50, 60, 70, 80])
                self.moveX = [(self.movement[1][0] - self.movement[0][0])/speed, 0, speed]
                self.moveY = [(self.movement[1][1] - self.movement[0][1])/speed, 0, speed]
                return
            if movement == 'Friend':
                friend = random.choice(self.friends)
                self.movement[1] = friend.location
                speed = random.choice([20, 30, 40, 50, 60, 70, 80])
                self.moveX = [(self.movement[1][0] - self.movement[0][0])/speed, 0, speed]
                self.moveY = [(self.movement[1][1] - self.movement[0][1])/speed, 0, speed]
                return
        else:
            self.movement[1] = self.home.location
            speed = random.choice([20, 30, 40, 50, 60, 70, 80])
            self.moveX = [(self.movement[1][0] - self.movement[0][0])/speed, 0, speed]
            self.moveY = [(self.movement[1][1] - self.movement[0][1])/speed, 0, speed]
            return

    def isHome(self):
        if (self.location[0]-100 <= self.home.location[0] <= self.location[0]+100) and (self.location[1]-100 <= self.home.location[1] <= self.location[1]+100):
            return True
        else:
            return False

    # Moves the person according to their random moving variable and ensures that people stay within the town boundaries
    def move(self,size):
        xmax, ymax, xmin, ymin = size[0], size[1], 10, 10
        if (self.location[0]-100 <= self.movement[1][0] <= self.location[0]+100) and (self.location[1]-100 <= self.movement[1][1] <= self.location[1]+100):
            self.initializeMotion()
        else:
            x, y = self.location[0], self.location[1]
            self.location = (x+self.moveX[0], y+self.moveY[0])
            self.quadrant = (self.location[0]%10, self.location[1]%10)
            self.moveX[1] += 1
            self.moveY[1] += 1
        if self.Infective[0]:
            self.check_recovery()

    # Increments the invective person's recovery by 1 hr until 2 weeks is reached, and the person becomes either recovered or dead
    def check_recovery(self):
        if self.Infective[1] < self.parameters.recoveryTime:
            self.Infective[1] += 1
            return
        if self.Infective[1] >= self.parameters.recoveryTime:
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