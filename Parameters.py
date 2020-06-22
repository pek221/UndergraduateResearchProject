
class Parameters:

    #The parameters used for the simulation
    def __init__(self):
        self.infectionRadius = 10
        self.infectionRate = 0.3
        self.recoveryRate = 0.95
        self.deathRate = 0.05
        self.initialProbabilityInfected = 0.01 #start with 1% of population infected