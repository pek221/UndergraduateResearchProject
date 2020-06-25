
class Parameters:

    #The parameters used for the simulation
    def __init__(self):
        self.infectionRadius = 2
        self.infectionRate = 0.35
        self.recoveryRate = 0.95
        self.recoveryTime = 336
        self.deathRate = 0.05
        self.initialProbabilityInfected = 0.01 #start with 1% of population infected
        self.probGoShopping = 0.05
        self.probVisitFriend = 0.1
        self.probStayHome = 0.85