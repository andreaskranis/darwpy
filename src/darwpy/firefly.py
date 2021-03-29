import math
import random
import numpy as np
import matplotlib.pyplot as plt


class Firefly(object):
    """ Simulates a firefly """

    def __init__(self,ranges,fitness_func,beta0=1.0,gamma=0.1,id=0):
        """ Sets up the firefly  """
        self.min_ranges = [ranges[r]['min'] for r in ranges]               #to ensure firefly will remain with the appropriate N-space for the problem
        self.max_ranges = [ranges[r]['max'] for r in ranges]               #same for the maximum
        self.position = np.array([ranges[r]['init'] for r in ranges])      #assign the initial value to each variable
        self.best_pos = self.position.copy()                       #ensure that no shallow copy will occur
        self.fitness_func = fitness_func
        self.intensity = self.update_intensity(self.position)
        self.best_intensity = self.update_intensity(self.best_pos)
        self.beta0 = float(beta0)                                  #baseline attractiveness at r=0
        self.gamma = float(gamma)                                  #aborption
        self.id = id
        self.dimensions = len(self.position)                       #just get the number of solutions

    def distance(self, partner):
        """ Returns the distance r between fireflies as the cartesian(eucleidian) distence """
        return np.linalg.norm(partner.position-self.position)  #same as: ((partner.position-self.position)**2).sum(axis=0)

    def attraction(self, partner):
        """ Returns the attractiveness beta between fireflies"""
        #return self.beta0 * math.exp(-self.gamma * (self.distance(partner)**2))
        return self.beta0/(1+self.gamma*(self.distance(partner)**2))

    def update_intensity(self,pos,minimise=True):
        """ Evaluates the fitness function given a position in N-dimensions
            If it is a minimisation problem, returns the inverse
        """
        if minimise:
            return 1./(self.fitness_func(pos)+1)
        return self.fitness_func(pos)+1
    

    def candidate_position(self,partner,step=0.5):
        """ Returns the new position """
        beta = self.attraction(partner)
        #rand_p = random.random()                         ## this would add the same random component, ie they would move in a diagonal from main
        rand_p = np.random.random(size=self.dimensions)   ## to make sure that I add a different random component in every dimension
        new_pos = self.position + beta*(partner.position - self.position) + step*(rand_p-0.5)
        return np.clip(new_pos,self.min_ranges,self.max_ranges)

    def move_if_better(self,partner,step=0.5):
        """  """
        if self.intensity <= partner.intensity:
            #print "I will move firefly %s given firefly %s becasuase my intensity %s < %s" % (self.id,partner.id,self.intensity,partner.intensity)
            #print "  my old pos was: %s" % self.position
            self.position = self.candidate_position(partner,step=step)
            self.intensity = self.update_intensity(self.position)
            #print "  my new pos is: %s with intensity %s" % (self.position,self.intensity)
            if self.intensity > self.best_intensity:
                self.best_intensity = self.intensity
                self.best_pos = self.position
        else:
            #print "** I will not move firefly %s given firefly %s becasuase my intensity %s > %s" % (self.id,partner.id,self.intensity,partner.intensity)
            pass

    def info(self):
        """ Helper function for de-bugging that shows Firefly() attributes """
        print("firefly initial id:{}".format(self.id))
        print("Current position  :{}".format(self.position))
        print("Best position     :{}".format(self.best_pos))
        print("Current intensity :{}".format(self.intensity))
        print("Best intensity    :{}".format(self.best_intensity))
        print("Absorption        :{}".format(self.gamma))
        print("------------------")

class FireflyPop(object):

    def __init__(self,ranges,fit_func):
        self.fireflies = [Firefly(ranges,fit_func,id=i) for i,r in enumerate(ranges)]
        self.N = len(self.fireflies)
        self.fit_func = fit_func
        self.sort_on_intensities()

    def change_absorption(self,new_absorption):
        if not isinstance(new_absorption,list):
            new_absorption = [new_absorption for i in range(len(self.fireflies))]

        for f,a in zip(self.fireflies,new_absorption):
            f.gamma = a

    def sort_on_intensities(self):
        self.fireflies.sort(key=lambda x:x.intensity,reverse=True)

    def sort_on_best_intensities(self):
        self.fireflies.sort(key=lambda x:x.best_intensity,reverse=True)

    def get_leader(self):
        return self.fireflies[0]

    def print_intensities(self):
        print("Ids    : {}".format([f.id for f in self.fireflies]))
        print("Current: {}".format([f.intensity for f in self.fireflies]))
        print("Best   : {}".format([f.best_intensity for f in self.fireflies]))

    def update(self,step=1):
        for i in range(self.N):
            for j in range(self.N):
                self.fireflies[i].move_if_better(self.fireflies[j],step=step)
        self.sort_on_intensities()

    def evolve(self,iterations,step=1):
        for i in range(iterations):
            self.update(step)
        self.sort_on_intensities()

    def go_to_bestSol(self):
        """ Returns the fireflies to their best (so-far) solution to search again """
        self.sort_on_best_intensities()
        for f in self.fireflies:
            f.position = f.best_pos
            f.intensity = f.best_intensity

    def get_best_sol(self):
        self.sort_on_best_intensities()
        return self.get_leader().best_pos


    ### only for 2D problems, debugging purposes
    def viz_sol(self,dim_X=0,dim_Y=1):
        """ Visualises two dimensions, just provide the idx in pos as dim_X and dim_Y """
        l = self.get_leader()
        step_x = float(l.max_ranges[dim_X]-l.min_ranges[dim_X])/100
        x = np.arange(l.min_ranges[dim_X],l.max_ranges[dim_X]+step_x,step_x)

        step_y = float(l.max_ranges[dim_Y]-l.min_ranges[dim_Y])/100
        y = np.arange(l.min_ranges[dim_Y],l.max_ranges[dim_Y]+step_y,step_y)

        X, Y = np.meshgrid(x, y)
        Z = [ [self.fit_func([ix,iy]) for iy in y] for ix in x]

        cs = plt.contour(X, Y, Z)
        for f in self.fireflies:
            plt.plot(f.position[dim_X],f.position[dim_Y],'bx')
        for f in self.fireflies:
            plt.plot(f.position[dim_X],f.position[dim_Y],'ro')
        plt.plot(l.position[dim_X],l.position[dim_Y],'go')
        return cs


    
    

############### RANGES ###############
def wordRanges(target_word,absMin=32,absMax=123):
    """ @desc:     Constructs an array with legal ranges and initial values
        @input:
        @output:   An array of dicts
        @comments: User tailor-mades this function to match specs of the domain/problem
                   I use the ascii code so absMin=32(space) (http://www.asciitable.com/)
        @warnings: This is not the same as in my GA/DE/SimAnnul
        @date:     v0.01 - 05/10/14
    """
    ranges = []
    for i,tr in enumerate(target_word):
        ranges.append({'min': absMin, 'max': absMax, 'type': int,'init':random.randrange(absMin,absMax) })
    return ranges


def xRanges(l=2,absMin=-100,absMax=100,init_func=None,init_params=[]):
    if not init_func:
        init_func = lambda x1,x2 : random.randrange(x1,x2)
        init_params = [absMin,absMax]

    ranges = []
    for i,tr in enumerate(range(l)):
        ranges.append({'min': absMin, 'max': absMax, 'type': float,'init': init_func(*init_params)})
    return ranges

################ FITNESS ################
def de_jong(pos):
    return np.power(pos,2).sum()

def schwefel(pos):
  return -pos[0]*math.sin(math.sqrt(abs(pos[0]))) - pos[1]*math.sin(math.sqrt(abs(pos[1])))

def rastrigin(pos):
    return (10 * 2 + (pow(pos[0], 2) - 10 * math.cos(2 * math.pi * pos[0])) + pow(pos[1], 2) - 10 * math.cos(2 * math.pi * pos[1]))

def crazy_landscape(pos):
    if (2<pos[0]<3) and (2<pos[1]<3):
        return 50
    if (8<pos[0]<9) and (-8<pos[1]<9):
        return 10
    if (-1<pos[0]<1) and (-1<pos[1]<1):
        return 5
    if (-3.2<pos[0]<-3) and (-3.2<pos[1]<-3):
        return 0
    return abs(20+100*random.random())



"""
### code that works!

reload(af)

f1 = af.Firefly(r1,af.de_jong)
f2 = af.Firefly(r2,af.de_jong)

r3 = [{'init': 3, 'max': 100, 'min': 0, 'type': float},{'init': 4, 'max': 100, 'min': 0, 'type': float}]
f3 = af.Firefly(r3,af.de_jong)

f1.update(f2)



###
N = 10
ranges = [af.xRanges() for i in range(N)]
p = af.Pop(ranges,af.de_jong)
p.viz_sol()
p.evolve(10)
p.viz_sol()
p.get_leader().info()





"""
