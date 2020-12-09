
import numpy as np


def draw_sol(domain_gene):
    """ Given the <domain>, draw a valid solution for gene <i> """
    if domain_gene.get('func',None):
        return domain_gene['func']()
    return np.random.uniform(low=domain_gene['min'], high=domain_gene['max']) 
        
    
def mutate(sol,domain,mut_prob=0.02,mut_idx=[]):
    """ Mutates a solution
    
    Args:
        sol (np.array)  : A solution vector [vector inlclues only genes]
        domain (dict)   : The DOMAIN dictionary containing info for each gene
        mut_prob (float): The probability to mutate each gene [0,1]
        mut_idx (list)  : If provided, will only mutate (with mut_prob=1) these indeces
        
    Returns:
        np.array: The (mutated) solution
    
    Note:
        No checks on <mut_prob> to ensure it is within [0,1]
        No checks if indeces in mut_idx are outside the size of <sol> and <domain>
    """
    if not mut_idx:
        mut_idx = np.where(np.random.random(size=len(sol)) <= mut_prob)[0] 
    for i in mut_idx:
        sol[i] = draw_sol(domain[i])
    return sol
    

def recombine(sol1,sol2,recomb_events=1,hot_regions=None):
    """ Recombines sol1 and sol2
    
    Args:
        sol1 (np.array)    : The solution vector for parent 1 [vector inlclues only genes]
        sol1 (np.array)    : The solution vector for parent 2 [vector inlclues only genes]
        recomb_events (int): The number of recombinations taking place
        hot_regions (list) : Default is None, but if supplied sum(hot_regions) = 1
                             The probabilites of recomb for each locus in sol 
    Returns:
        np.array: The recombined solution
        
    Note:
        
    """
    if recomb_events >= len(sol1):
        recomb_events = len(sol1) - 1 
    
    parent_sol = {0:sol1, 1:sol2}                                              # This allows switching solutions
    if recomb_events < 1:
        return parent_sol[np.random.randint(0,2)]

    sol = np.ones(shape=len(sol1)) * -9
    break_points = np.sort(np.random.choice(range(len(sol1)),size=recomb_events\
                                            ,replace=False,p=hot_regions))+1
    st = 0                                                                      
    st_strand = np.random.randint(0,2)                                         # The starting solutions
    for i,b in enumerate(break_points):
        sol[st:b] = parent_sol[(i+st_strand)%2][st:b]
        st = b
    if st == len(sol1):                                                        # If the last breakpoint is after the end of the solution, this will create problens
        sol[st-1] = parent_sol[(i+st_strand+1)%2][st-1]
    else:
        sol[st:] = parent_sol[(i+st_strand+1)%2][st:]
    return sol
    
def evaluate(pop,fitness_func,fit_col=-1,extra_cols=2):
    """
    
    Args
        pop (np.array)     : The matrix of solution to score
        fitness_func  (obj): The fitness function
        
    Returns
        np.array :
    
    """
    for i in range(pop.shape[0]):
        pop[i,fit_col] = fitness_func(pop[i,:-extra_cols])
    return pop


def init_pop(N,domain,fitness_func,extra_cols=2):
    """ Initialises the opulation with either custom or random values
    
    Args:
        N             (int): The size of the population (genome)
        domain       (dict): A <DOMAIN> dictionary
        fitness_func (func): The fitness function

    Returns:
        np.array  : The intiated populaiton
    
    Note:
        If <DOMAIN> contains an 'init' attribute, this value will be used
    
    """
    pop = np.zeros((N,len(domain)+extra_cols))
    for i in range(N):
        for j in sorted(domain.keys()):
            if domain[j].get('init',None):
                pop[i,j] = domain[j]['init']
            else:
                pop[i,j] = draw_sol(domain[j])
        #pop[i,:-2] = np.array([np.random.randint(domain[j]['min'],domain[j]['max'])  for j in sorted(domain.keys())])
        pop[i,-1]  = fitness_func(pop[i,:-extra_cols])
    return pop

def sort_pop(pop,gen_col=-2,fit_col=-1):
    """
    
    Args
        pop (np.array): TYPE
        gen_col (int): TYPE, optional
        fit_col (int): TYPE, optional

    Returns
        np.array : The sorted <POP> 2d array accroding to the criteria
        
    Note
        Currently sorting on fitness,generations that tends to keep older (good)
        solutions in the population
    """
    ##[opt1] Sort only on fitness
    #return pop[pop[:,fit_col].argsort()]
    
    ##[opt2] Sort on fitness and then generation (this keeps the oldest parents in the population)
    sorted_idx = np.lexsort((pop[:,gen_col],pop[:,fit_col]))
    return pop[sorted_idx]


################
## STRATEGIES ##
################
def strategy_breed(parents,nkids,domain,genN,recomb_events=1,pS1=0.2,mut_prob=0.2):
    """ Get the next generation by rotating the elite parents
         
    Args
        parents (np.array): The 2D matrix with the parents (last column is fitness)
        nkids (int)       : The number of kids to produce
        domain (dict)     :
        genN (int)        : The generation number to mark in kids
        pS1 (float)       : The proportion of elite parents [0-1 range]
        mut_prob (float)  : The mutation probability to pass to mutate()
    
    Returns
        np.array : a 2D matrix with the new kids 
    
    """
    ##
    n,m = parents.shape
    kids = np.zeros((nkids,m))
    nS1 = int(n * pS1)
    P = set(range(n))
    
    ##[TODO] Analyse diversity to decide mutation/recombination
    ##[TODO] Modify domains according to diversity; influence in fitness

    kid_idx = 0
    while kid_idx < nkids:
        for p1 in range(nS1):
            S2 = np.random.permutation(list(P.difference([p1])))
            for p2 in S2:
                k = mutate(recombine(parents[p1,:-2],parents[p2,:-2],recomb_events=recomb_events),domain,mut_prob=mut_prob)
                kids[kid_idx,:-2] = k
                kids[kid_idx,-2] = genN
                kid_idx +=1
                if kid_idx == nkids:
                    break
            if kid_idx == nkids:
                break
    return kids
    
    

##DELETE
#def domain_dummy(n,m1=-5,m2=5):
#    out = {}
#    for i in range(n):
#        out[i] = {'min':m1,'max':m2,'init':np.random.randint(m1,m2),'min0':m1,'max0':m2}
#    return out
    
    
    
        
    















