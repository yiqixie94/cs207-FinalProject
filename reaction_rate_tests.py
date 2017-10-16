# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 17:50:51 2017

@author: Camilo
"""

import Reaction
import ReactionSystem
import numpy as np

### Tests for ReactionSystems:
   
def test_reaction_system_nu_1():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':1}))
    reactions.append(Reaction(reactants={'A':1,'C':2}, products = {'D':4}))
    
    rs = ReactionSystem(reactions)
    nu_1 = rs.calculate_nu_1()
    nu_2 = rs.calculate_nu_2()
    
    assert( nu_1 == [[1,1],[2,0],[0,2],[0,0]] )
    assert( nu_2 == [[0,0],[0,0],[2,0],[0,4]] )
    

def test_reaction_system_progress_rate():
    
    reactions = []
    reactions.append(Reaction(reactants={'A':1,'B':2}, products = {'C':2}, coeffLaw = 'const', coeffParams = 10))
    reactions.append(Reaction(reactants={'A':2,'C':2}, products = {'B':1, 'C':1}, coeffLaw = 'const', coeffParams = 10))
    
    concentrations = [1,2,1]
    rs = ReactionSystem(reactions, concentrations)
    prog_rate = rs.get_progress_rate_system()
            
    assert(prog_rate==[40,10])
    
def test_reaction_system_reaction_rate():
    
    
    assert(np.array_equal(rrs.reac_rate_system([1,2,0.5],np.array([[1,2,0]]), np.array([[0,0,1]]), [10]),[-40, -80,  40]))
    
    
    
    