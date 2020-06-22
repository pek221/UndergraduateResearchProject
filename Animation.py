import pygame

class Animation:

    # Initializes the animation
    def __init__(self,size):
        self.size = size
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("COVID-19 Model")
        self.background = self.screen.convert()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

    # Is called every hour to update the animation
    def update_animation(self,town,t):
        self.screen.fill((0,0,0))
        Animation.drawTime(self,t)
        Animation.drawPeople(self,town)
        pygame.display.flip()

    # Displays the time in the top right corner of the animation (in days)
    def drawTime(self,t):
        text = self.font.render("Day: %02d"%(t/24), True, (255,255,255),(0,0,0))
        textrect = text.get_rect()
        textrect.centerx = 450
        textrect.centery = 30
        self.screen.blit(text,textrect)

    # For each person in the population, draws a small dot of the color corresponding to the condition of the given person and their location
    def drawPeople(self,town):
        for p in town.population:
            if p.Susceptible == True:
                color = (255,255,0)
            elif p.Infective[0] == True:
                color = (200,0,0)
            elif p.Recovered == True:
                color = (0,0,200)
            elif p.Dead == True:
                color = (0,0,0)#Remove the person from screen
            pygame.draw.circle(self.screen, color, (p.location[0]/100,p.location[1]/100),5)