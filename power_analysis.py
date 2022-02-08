import pandas
import pymc3 as pm
import warnings
import arviz as az
import numpy as np 
from matplotlib import pyplot as plt
warnings.filterwarnings('ignore')


class simulations: 
    
    def __init__(
        self,
        v_observations,
        v_conversions, 
        c_observations, 
        c_conversions,
        n_samples = 1000,
        
    ):
        self.n_samples = n_samples
        self.v_observations = v_observations
        self.v_conversions = v_conversions
        self.c_observations = c_observations
        self.c_conversions = c_conversions 
        self.v_current_trace = 1 
        self.c_current_trace = 1
        self.difference = self.v_current_trace - self.c_current_trace
        self.rel_difference=100*(self.v_current_trace-self.c_current_trace)/self.v_current_trace
        self.hdi_prob = 0.95
        
    def run_models(self):
        
        with pm.Model() as control:

            #Prior
            prior=pm.Beta('Control', alpha = 1, beta= 1)  

            #fit the observed data
            obs=pm.Binomial("Observed", n=self.c_observations, p=prior, observed=self.c_conversions)

            trace_control = pm.sample(self.n_samples)
            self.c_current_trace = trace_control['Control']


        with pm.Model() as variant:
            #Prior
            prior=pm.Beta('Variant', alpha=1, beta=1)  

            #fit the observed data to our model 
            obs=pm.Binomial("Observed", n=self.v_observations, p=prior, observed=self.v_conversions)

            trace_variant = pm.sample(self.n_samples)
            self.v_current_trace = trace_variant['Variant']
    
    
    def check_significance(self, absolute = False):

        #Not all values of hdi_prob area allowed

        lower = round(((1-(self.hdi_prob))/2)*100, 1)
        upper = 100*self.hdi_prob+lower
        
        data = self.rel_difference
        
        if absolute: 
            data = self.difference
        

        summary = az.summary(data, hdi_prob=self.hdi_prob)

        assert summary.columns[2] == 'hdi_{}%'.format(lower)
        assert summary.columns[3] == 'hdi_{}%'.format(upper)


        return(
            not summary['hdi_{}%'.format(lower)][0] <= 0 <=  summary['hdi_{}%'.format(upper)][0], 
            summary['hdi_{}%'.format(lower)][0],
            summary['hdi_{}%'.format(upper)][0]
        )
    
    def get_probability(self, threshold = None): 
        
        
        
        return(f'Probability that Variant is better: {(self.v_current_trace > self.c_current_trace).mean():.1%}.')
    
        
    
    
    

    
    