import pygame
from Town import Town
from Parameters import Parameters
from Animation import Animation
import pandas as pd
import  matplotlib.pyplot as plt

class World:

    def __init__(self):
        self.townSize = (50000,50000)
        self.parameters = Parameters()
        self.clock = pygame.time.Clock()

    # This simulation runs for half a year, with each iteration of the for loop being 1 hour
    def runSimulation(self, fps =30, initialTime=0, finalTime=2000):

        # Create animation and population for Bethlehem, Allentown, etc.
        bethlehemAnimation = Animation((self.townSize[0]/100,self.townSize[1]/100))
        bethlehem = Town(300,self.townSize,self.parameters)
        allentownAnimation = Animation((self.townSize[0]/100,self.townSize[1]/100))
        #allentown = Town(300,self.townSize,self.parameters)

        # Print Initial Conditions of Each Population
        print "Initial Conditions for Bethlehem:"
        bethlehem.evaluatePopulation(0)
        #print "Initial Conditions for Allentown:"
        #allentown.evaluatePopulation(0)

        # Each iteration of this for loop represents 1 hour
        for t in xrange(initialTime,finalTime):
            #print "Day: %01d, Hour: %01d \n"%(t/24, t%24)

            # Gather data from the current population and add it to the data dictionary
            bethlehem.get_data(t)
            #allentown.get_data(t)

            # Update the animation to represent the location and condition of each person in the population
            bethlehemAnimation.update_animation(bethlehem,t)
            #allentownAnimation.update_animation(allentown,t)

            # Update the locations and conditions of each town's population
            bethlehem.update_locations()
            bethlehem.update_conditions()
            #allentown.update_locations()
            #allentown.update_conditions()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.clock.tick(fps)

        # Print the final conditions for each town
        print "Final Conditions for Bethlehem:"
        bethlehem.evaluatePopulation(4380)
        #print "Final Conditions for Allentown:"
        #allentown.evaluatePopulation(4380)

        bethlehemdf = pd.DataFrame(bethlehem.data, columns=['Time', 'Susceptible', 'Infective', 'Recovered', 'Dead'])
        #allentowndf = pd.DataFrame(allentown.data, columns=['Time', 'S', 'I', 'R', 'D'])

        plt.plot('Time','Susceptible', data=bethlehemdf, color='y', linewidth=2)
        plt.plot('Time', 'Infective', data=bethlehemdf, color='r', linewidth=2)
        plt.plot('Time', 'Recovered', data=bethlehemdf, color='b', linewidth=2)
        plt.plot('Time', 'Dead', data=bethlehemdf, color='k', linewidth=2)
        plt.legend()

        #bethlehemdf.plot.line()
        plt.show()


        #with pd.ExcelWriter(r'C:\Users\Pierr\Desktop\PyCharm\UndergradResearchProject\data\export_dataframe2.0.xlsx') as writer:
        #    bethlehemdf.to_excel(writer, sheet_name='Bethlehem', index=False, header=True)
            #allentowndf.to_excel(writer, sheet_name='Allentown')