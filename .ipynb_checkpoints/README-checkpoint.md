# Bayesian power simulations

## Background
This script should enable time estimations until significance is determined using bayesian beta-binomial combinattion. This is done by 
executing two parallel posterior distributions where one is manipulated to show increased or decreased performance over time. This simulation can help you with: 

1. Not panicking when a significant drop happens on the first day of test. 
2. Properly picking your primary metrics when having tight deadlines. 
2. Setting expectations of a test before a test is launched. 

## Run test 
Run the scrip, add your data points and the number of days you want to simulate. Input date could be tweaked.


## Example 

``python run power.py [1000, 1000, 20, 20, "day", "False"]``










