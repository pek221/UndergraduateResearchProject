import random
from Person import Person
from Building import Building

class Town:

    # Initializes the town and creates a person object for each member of the population
    def __init__(self,popSize, townSize,parameters):
        self.popSize = popSize
        self.data = {'Time': [], 'Susceptible': [], 'Infective': [], 'Recovered': [], 'Dead': []}
        self.townSize = townSize
        self.parameters = parameters
        self.population = []
        self.buildings = []
        self.initializeBuildingsAndPopulation()

    def initializeBuildingsAndPopulation(self):
        # Initialize Buildings
        step = self.townSize[0]/11
        for x in range(step,10*step,step):
            for y in range(step,10*step,step):
                self.buildings.append(Building('House',(x,y),[0,random.randint(1,6)]))
        mid = len(self.buildings)/2
        self.buildings[mid].type = 'Store'
        self.buildings[mid].capacity = [0,0]
        #Initialize population
        infective = int(self.parameters.initialProbabilityInfected * 100)
        susceptible = 100 - infective
        my_list = ['I'] * infective + ['S'] * susceptible
        for i in range(self.popSize):
            for b in self.buildings:
                if b.capacity[0] < b.capacity[1]:
                    friends = self.findFriends(b)
                    initialCondition = random.choice(my_list)
                    if initialCondition == 'I':
                        self.population.append(Person(i + 1, b.location[0], b.location[1], False, True, b, self.buildings[mid], friends))
                    else:
                        self.population.append(Person(i + 1, b.location[0], b.location[1], True, False, b, self.buildings[mid], friends))
                    b.capacity[0] += 1
                    break

    def findFriends(self,home):
        n = len(self.buildings)
        friends = []
        while len(friends)<5:
            temp = random.choice(self.buildings)
            if temp != home:
                friends.append(temp)
        return friends

    # This method loops through the population and prints out the number of people in each category
    def evaluatePopulation(self, t):
        susceptible, infective, recovered, dead = 0, 0, 0, 0
        for p in self.population:
            if p.Susceptible:
                susceptible += 1
            elif p.Infective[0]:
                infective += 1
            elif p.Recovered:
                recovered += 1
            elif p.Dead:
                dead += 1
        print "WEEK %d: \nPopulation Size: %d \nSusceptible: %d \nInfective: %d \nRecovered: %d \nDead: %d" %(t / 168,len(self.population), susceptible, infective, recovered, dead)

    # This method adds the conditions of the population to a dictionary which will be used to create graphs of the simulation
    def get_data(self, t):
        susceptible, infective, recovered, dead = 0, 0, 0, 0
        for p in self.population:
            if p.Susceptible:
                susceptible += 1
            elif p.Infective[0]:
                infective += 1
            elif p.Recovered:
                recovered += 1
            elif p.Dead:
                dead += 1
        self.data['Time'].append(int(t/24))
        self.data['Susceptible'].append(susceptible)
        self.data['Infective'].append(infective)
        self.data['Recovered'].append(recovered)
        self.data['Dead'].append(dead)

    # This method updates the location of each person in the population
    def update_locations(self):
        for person in self.population:
            person.move(self.townSize)

    # This method updates the condition of each person in the population
    def update_conditions(self):
        for person in self.population:
            if person.Infective[0] == True:
                neighbors = person.find_neighbors(self.population)
                person.try_to_infect_neighbors(neighbors, self.parameters.infectionRate)
