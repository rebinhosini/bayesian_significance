import pandas
import pymc3 as pm
import warnings
import arviz as az
import numpy as np 
import seaborn as sns
from matplotlib import pyplot as plt
warnings.filterwarnings('ignore')

class beta_binomial_testing: 
    
    def __init__(
        self,
        v_observations,
        v_conversions, 
        c_observations, 
        c_conversions,
        n_samples = 5000,
        
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

        diff = self.v_current_trace - self.c_current_trace
        output = 100*diff/self.c_current_trace
        
        if absolute: 
            output = diff
        
        summary = az.summary(output, hdi_prob=self.hdi_prob)

        assert summary.columns[2] == 'hdi_{}%'.format(lower), "hdi not found"
        assert summary.columns[3] == 'hdi_{}%'.format(upper), "hdi not found"
    
        return(
            not summary['hdi_{}%'.format(lower)][0] <= 0 <=  summary['hdi_{}%'.format(upper)][0], 
            summary['hdi_{}%'.format(lower)][0],
            summary['hdi_{}%'.format(upper)][0]
        )
    
    
    def plot_distributions(self): 
        plt.rcParams["figure.figsize"] = (20,4)
        sns.distplot(self.c_current_trace, bins=40, label='posterior of control')
        sns.distplot(self.v_current_trace, bins=40, label='posterior of variant')
        plt.xlabel('Rate')
        plt.ylabel('Density')
        plt.title("Posterior distributions of the control and variant conversion rates")
        plt.legend()
        plt.show()
        
    def plot_posterior_difference(self, relative = False):
        plt.rcParams["figure.figsize"] = (20,4)
        if relative:
            sns.distplot(((self.v_current_trace-self.c_current_trace)/self.c_current_trace)*100, label='Relative between control and variant posterior distributions', bins = 40)
            plt.xlabel('Uplift %')
            plt.ylabel('Density')
            plt.title("Uplift between control and variant")
        else:
            sns.distplot(self.v_current_trace-self.c_current_trace, label='Difference between control and variant posterior distributions', bins = 40)
            plt.xlabel('Rate')
            plt.ylabel('Density')
            plt.title("Posterior difference")
        plt.legend()
        plt.show()
        
    def get_probability(self): 
        print(f'Probability that variant is better: {(self.v_current_trace > self.c_current_trace).mean():.1%}.')
        print(f'Probability that control is better: {(self.c_current_trace > self.v_current_trace).mean():.1%}.')
    
        
    
    
    
        
    
    
    

    
    