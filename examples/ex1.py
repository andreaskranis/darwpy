import numpy as np
import darwpy as d
import pprint as pp
from functools import partial
import math

CL = 2
G = 100
N = 500
nPAR = 10
nKIDS = N - nPAR
    

def create_reference_solution(chromosome_length):
    number_of_ones = int(chromosome_length / 2)
    # Build an array with an equal mix of zero and ones
    reference = np.zeros(chromosome_length)
    reference[0: number_of_ones] = 1
    # Shuffle the array to mix the zeros and ones
    np.random.shuffle(reference)
    
    return reference


def fitness(sol,x=[]):
    x = sol
    d = len(x)
    return 418.9829*d - sum(x*np.sin(np.sqrt(np.abs(x))))
    #w,x,y,z = sol
    #return (-2 * (w ** 2) + math.sqrt(abs(w)) - (x ** 2) + (6 * x) - (y ** 2) - (2 * y) - (z ** 2))
    

def sort_pop(pop,fit_col=-1):
    return pop[pop[:,fit_col].argsort()]
    


def main():
    #ref = create_reference_solution(CL)
    #fitness = partial(create_fitness, reference=ref)
    
    domain = d.domain_dummy(CL,-500,500)    
    
    pop = d.init_pop(N, domain, fitness)
    pop = sort_pop(pop,fit_col=-1)
    #pp.pprint(pop)

    for gen in range(G):
        new_pop = np.zeros((pop.shape))
        parents = pop[:nPAR,:]
        kids = d.breed(parents,nKIDS,domain,pS1=0.2,mut_prob=0.2)
        
        new_pop[:nPAR,:] = parents
        new_pop[nPAR:,:] = kids
        new_pop = d.evaluate(new_pop,fitness)
        
        pop = sort_pop(new_pop,fit_col=-1)
        #pp.pprint(pop)

        print(f"Best fitness {pop[0,-1]}")
        #print(f"REF:{ref}")
        #print(f"ALT:{pop[0,:-1]}, {pop[0,-1]}")
    print(f"best sol: {pop[0,:-1]}")

if __name__ == "__main__":
    main()