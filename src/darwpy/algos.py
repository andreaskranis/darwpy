#!/usr/bin/env python3

import numpy as np
from scipy import stats
import functools
from . import operators as o


#from tqdm import tqdm
try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x:x


def check_convergence(func):
    ### these could be arguments of the check_convergence
    PROP = 0.5
    #ITERS = 10                        
    
    @functools.wraps(func)
    def wrapper_opt(*args, **kwargs):
        ITERS = 10
        pop = []
        while 1:        
            ITERS -= 1
            if ITERS == 0:
                break
            kwargs['pop'] = pop                           ##this allow me to start the new iteration from the last point and not from a random point
            pop,fitness_profile = func(*args, **kwargs)
            start = int(PROP*kwargs['generations'])
            slope, intercept, r_value, p_value, std_err = stats.linregress(x=list(range(start,kwargs['generations']+1)),y=fitness_profile[start:])
            print(f"The slope from {start} to end was {slope}")
            if -0.001 < slope:
                if kwargs.get('verbose',None):
                    print("Likely convergence to (global) minimum...")
                return pop,fitness_profile,slope            
            else:
                if kwargs.get('verbose',None):
                    print("Will run a new iterations using the most recent pop")

        return pop,fitness_profile,slope
    return wrapper_opt

@check_convergence
def GA(domain,fitness,N=50,nPAR=10,recomb_events=2,pS1=0.2,mut_prob=0.2,generations=1000,domain_gen=None,verbose=True,pop=[]):
    """ Runs a Genetic Algorithm
    
    Args:
        domain (dict)      : A <domain> dictionary
        fitness (func)     : A fitness function that accepts a sol
        N (int)            : The number of individuals per generation
        nPAR (int)         : The number of parents in each generation
        recomb_events (int): The number of recombination events
        pS1 (float)        : The proporion of elite parents [0-1 range]               
        mut_prob (float)   : The probability to mutate each gene [0,1]
        generations (int)  : The number of generations 
        
    Returns:
        (tuple): tuple containing:
            - np.array : The 2D array with the final solutions
            - np.array : The fitness profile as 1D
    """
    if not verbose:
        tqdm = lambda x:x
    else:
        try:
            from tqdm import tqdm
        except ImportError:
            tqdm = lambda x:x

    nKIDS = N - nPAR
    REPORT_EVERY = round(generations/4,0)
    report_idx = [0,1,int(nPAR/2),nPAR,nPAR+int(nKIDS/5)]    ##interesting animals to print stats
    fitness_profile = []
    
    if len(pop) == N:
        print("** Initial pop was provided by user")
    else:
        pop = o.init_pop(N, domain, fitness)
        pop = o.sort_pop(pop,fit_col=-1)
    
    fitness_profile.append({pop[0,-1]})
    print(f"Best initial fitness: {pop[0,-1]}")    
        

    for gen in tqdm(range(generations)):
        new_pop = np.zeros((pop.shape))
        parents = pop[:nPAR,:]
        kids = o.strategy_breed(parents,nKIDS,domain,gen,recomb_events=recomb_events,pS1=pS1,mut_prob=mut_prob)
        
        new_pop[:nPAR,:] = parents
        new_pop[nPAR:,:] = kids
        new_pop = o.evaluate(new_pop,fitness)
        pop = o.sort_pop(new_pop,fit_col=-1)
        fitness_profile.append(pop[0,-1])
        
        try:
            if gen %  REPORT_EVERY == 0:
                print(f"pop@{gen} [gen,fitness]: {['{}->{}'.format(ri,list(pop[ri,-2:])) for ri in report_idx]}")
        except ZeroDivisionError:
            pass

        ## experimental, probably remove [it allows to refresh domain, ie the sample function]
        if domain_gen:
            domain = domain_gen() 
    
    if verbose:        
        print("\n")
        print(f"Best fitness {pop[0,-1]}")
        print(f"best sol: {pop[0,:-2]} obtained in generation {pop[0,-2]}")
    return pop,fitness_profile



