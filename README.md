# fractional-matching

Generate the active and passive configurations for different problems obtained through round elimination

# File details

There are two folders round 2 and round-1-relax, each containing a python script for generating the active and passive configuration for their respective problems.

## Input Parameters

Both the scripts take exactly the same input, i.e. 3 space seperaed integers: n, act_deg and pass_deg which mean the following.
1. n is the fractional denominator used to denote that we consider all multiples of 1/n. 
2. act_deg denotes the degree of active nodes.
3. pass_deg denotes the degree of passive nodes.

For example, consider the input $2$ $3$ $4$. It means that we use fractional values $\{  0,1/2,1\}$, active nodes have degree $3$ and passive nodes have degree $4$. 

## Output Files

1. "round-1-relax-problem.py" files outputs the active and passive configuration in file named "configs-1-relax.txt"
2. "round-2-problem.py" files outputs the active and passive configuration in file named "configs-2.txt"