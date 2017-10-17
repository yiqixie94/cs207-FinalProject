
import numpy as np

class ReactionSystem:
    
    def __init__(self, reaction_ls, element_ls):
        self._num_reactions = len(reaction_ls)
        self._num_elements = len(element_ls)
        self._reaction_ls = reaction_ls
        self._element_ls = element_ls
        
    def set_conditions(self, **kwargs):
        # C: I believe that this should be changed to clearly indicate what are the possible inputs.
        if 'T' in kwargs:
            if (kwargs['T'] <= 0):
                raise ValueError("T = {0:18.16e}: Negative Temperature are prohibited.".format(T))
                
            self._T = kwargs['T']
            
        if 'concs' in kwargs:
            if (kwargs['concs'] != len(self._reaction_ls)):
                raise ValueError('The number of concentrations is different than the number of species')
            for conc in kwargs['concs']:
                if conc < 0:
                    raise ValueError('Negative concentrations are prohibited.')
                
            self._concentration_ls = kwargs['concs']
    
    def get_conditions(self):
        # I believe the dictionary is not necessary in this case
        return dict(T=self._T, concs=self._concentration_ls)
    
    def get_reaction_rate_coefs(self):
        self._k = np.zeros(self._num_reaction)
        for n, r in enumerate(self._reaction_ls):
            self._k[n] = r.rateCoeff(T = self._T)
            
        return self._k
    
    def calculate_nu_1(self):
        self._reactants = np.zeros([self._num_element, self._num_reaction])
        for n, r in enumerate(self._reaction_ls):
            for idx, e in enumerate(self._element_ls):
                self._reactants[idx, n] = r.getReactants()[e] if e in r.getReactants() else 0
        
        return self._reactants
    
    def calculate_nu_2(self):
        self._products = np.zeros([self._num_element, self._num_reaction])
        for n, r in enumerate(self._reaction_ls):
            for idx, e in enumerate(self._element_ls):
                self._products[idx, n] = r.getProducats()[e] if e in r.getProducats() else 0
                
        return self._products
    
    def get_progress_rate(self):
        self._k = self.rateCoeff()
        nu_react = self.calculate_nu_1()
        self.progress = self._k # Initialize progress rates with reaction rate coefficients
        for jdx, rj in enumerate(self.progress):
            if rj < 0:
                raise ValueError("k = {0:18.16e}:  Negative reaction rate coefficients are prohibited!".format(rj))
            for idx, xi in enumerate(self._concentration_ls):
                nu_ij = nu_react[idx,jdx]
                if xi  < 0.0:
                    raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
                if nu_ij < 0:
                    raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ij))

                self.progress[jdx] *= xi**nu_ij
        return self.progress
    
    def get_reac_rate(self):
        self.progress = self.get_progress_rate()
        nu_react = self.calculate_nu_1()
        nu_prod = self.calculate_nu_2()
        nu = nu_prod - nu_react
        self.reac_rate = np.dot(nu, self.progress)
        return self.reac_rate