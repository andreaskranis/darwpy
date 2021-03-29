# Darwpy

A light-weight, yet flexible library for optimisation using Evolutionary Algorithms. The library provides the functionality to monitor convergence and enable user to get an idea whether a global optimal has been reached. The implementation is designed to enable control of the underlying methods and parameters over the iterative process (e.g tweak the selection process). 

Currently only a Genetic Algorithm has been fully implemented. An experimental implementation of the (Firefly optimisation algorithm)[https://en.wikipedia.org/wiki/Firefly_algorithm] is also included. More algorthms, such as the Differential Evolution, will be implemented.

(Yabox)[https://github.com/pablormier/yabox] has been used as a paradigm for implementing Evolutionary Algorithms in Python. Darwpy models can be adapted to yabox ones and vice-versa. Check the notebooks for examples. The formulaiton of the test problems is heavily based from the code provided in yabox.

![Optimasation_example](docs/_static/Figure_2.png?raw=true)

## Installation

Clone the repository and use pip with -e flag to install


```bash
git clone https://github.com/andreaskranis/darwpy.git
pip install -e darwpy/
```

## Usage

See the the notebooks and scripts in the *example/* folder to get an overview using well known functions. For more functions, see this [link](https://www.sfu.ca/~ssurjano/optimization.html) 

In the simplest approach, user needs to specify a dictionary to describe the domain and a cost function. The domain dictionary has a special structure, as seen in the code snipper below


```python
import numpy as np
improt darwpy

def get_domain(bounds=[-5.12,5.12],dimensions=2):    
    """ """
    out = {}
    for i in range(dimensions):
        m1,m2 = bounds
        out[i] = {'min':m1,'max':m2,'init':np.random.randint(m1,m2),'min0':m1,'max0':m2}
    return out

def cost_func(sol):
    """Sphere function"""
    return sum(s**2 for s in sol)


domain = get_domain()
pop,fitness,slope = darwpy.GA(domain,cost_func,N=60,generations=2000)

print(pop1[0,:len(domain)])     ## The best solution
print(pop1[0,len(domain):])     ## The generation when the best solution was found and the corresponding value of the cost function 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[Apache Licence 2.0](https://choosealicense.com/licenses/apache-2.0/)