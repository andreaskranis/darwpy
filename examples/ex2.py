#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import darwpy as d
import problems as p

import sys
import inspect


def get_classes(module=sys.modules[__name__],exclude_names=set()):
    classes = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if obj.__name__ not in exclude_names:
                classes[obj.__name__] = obj
    return classes


def main():
    classes =get_classes(p,exclude_names=set([p.BaseProblem]))
    
    CHOICE='CrossInTray'
    problem = classes[CHOICE]()
    
    pop,fitness = d.GA(problem.domain,problem.evaluate,N=60,generations=2000)
    



if __name__ == "__main__":
    main()


