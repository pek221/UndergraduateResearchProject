import random
from Person import Person

class Town:

    # Initializes the town and creates a person object for each member of the population
    def __init__(self,popSize, townSize,parameters):
        self.popSize = popSize
        self.data = {'Time': [], 'S': [], 'I': [], 'R': [], 'D': []}
        self.townSize = townSize
        self.parameters = parameters
        self.population = []
        for i in range(self.popSize):
            x = random.randint(10, self.townSize[0] - 10)
            y = random.randint(10, self.townSize[1] - 10)
            infective = int(parameters.initialProbabilityInfected * 100)
            susceptible = 100 - infective
            my_list = ['I'] * infective + ['S'] * susceptible
            initialCondition = random.choice(my_list)
            if initialCondition == 'I':
                self.population.append(Person(i + 1, x, y, False, True))
            else:
                self.population.append(Person(i + 1, x, y, True, False))

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
        print "WEEK %d: \nSusceptible: %d \nInfective: %d \nRecovered: %d \nDead: %d" %(t / 168, susceptible, infective, recovered, dead)

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
        self.data['Time'].append(t)
        self.data['S'].append(susceptible)
        self.data['I'].append(infective)
        self.data['R'].append(recovered)
        self.data['D'].append(dead)

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
