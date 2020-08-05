
class Parameters:

    #The parameters used for the simulation
    def __init__(self):
        self.infectionRadius = 2
        self.infectionRate = 0.25
        self.recoveryRate = 0.95
        self.recoveryTime = 336 # 2 weeks
        self.deathRate = 0.05
        self.initialProbabilityInfected = 0.01 #start with 1% of population infected
        self.probGoShopping = 0.20
        self.probVisitFriend = 0.20
        self.probStayHome = 0.60