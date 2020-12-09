
import unittest

import numpy as np
import darwpy as d

class BasicTests(unittest.TestCase):
    
    
    
    
    
    
    ####################
    ## MUTATION TESTS ##
    ####################
    def test_mut_simple(self):
        """ Tests the mutation only for min-max   """
        domain = {0:{'min':0,'max':5},1:{'min':-5,'max':5}}
        sol = np.array([0,0])
        
        sol1 = d.mutate(sol,domain,mut_prob=0.5)
        print(f"mut_simple: {sol1}")
        self.assertTrue(0 <= sol1[0]  <= 5)        
        self.assertTrue(-5 <= sol1[1]  <= 5)


    def test_mut_customFunc(self):
        """ Tests the mutaiton, when a custom function is provided """
        def spec_func():
            a = np.random.randint(0,5)
            while a == 1:
                a = np.random.randint(0,5)
            return a
        
        domain = {0:{'min':0,'max':5},1:{'min':-5,'max':5},2:{'func':spec_func}}
        sol = np.array([0,0,0])
        
        sol1 = d.mutate(sol,domain,mut_prob=0.90)
        print(f"mut_customFunc: {sol1}")
        self.assertTrue(0 <= sol1[0]  <= 5)        
        self.assertTrue(-5 <= sol1[1]  <= 5)
        self.assertTrue(sol1[2] != 1)

    def test_mut_customProb(self):
        """ Tests the  """
        
        domain = {0:{'min':0,'max':5},1:{'min':-5,'max':5},2:{'min':-15,'max':15}}
        sol = np.array([0,0,0])
        
        sol1 = d.mutate(sol,domain,mut_prob=0.90,mut_idx=[2])
        print(f"mut_customProb: {sol1}")
        self.assertTrue(sol1[0]  == 0)        
        self.assertTrue(sol1[1]  == 0)
        self.assertTrue(-15 <= sol1[2]  <= 15)


    ##################
    ## RECOMB TESTS ## 
    ##################
    def test_recomb(self):
        """ Test the recombination and the hot_regions provided """
        sol1, sol2 = [0,0,0,0],[1,1,1,1]
        hot_regions = [0,0,0,1]                  ##NOTE: sum(hot_regions) shouls always be 1
        rec_events = 1
        sol = list(d.recombine(sol1,sol2,rec_events,hot_regions))
        print(f"recomb sol: {sol}")
        self.assertTrue( (sol == [0,0,0,1]) or (sol == [1,1,1,0])  )