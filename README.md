decision-net
============
# ${1:Decision Net}
Decision nets used as a computation model for how people explain behavior.

 
## Installation
 
Depends on numpy and matplotlib.
 
## Usage
 
decision_net.py contains the code used for the project. It has methods to compute the complexity of each network and the utility of a network. Input is the network, knowledge values and decision values and it will output the complexity, utility and predictions.

To run the code as is, simply clone and run:
$ python decision_net.py
in a terminal. It will run the code, output the results and generate the plots.

## Plotting

plot.py handles most of the plotting for the experiment. It generates the plots for both experiments. The data we collected is also contained here in the get_exp_data method. Each case is broken into 2 groups of 15, but combined before plotting.

## Network Structure

The network structure, as seen in the seat_network_x1.py file, is a JSON object with a list of nodes and special properties. The list of nodes contains all the nodes. Each node has a unique id, name, list of parents,  type (either chance, decision or utility) and a CPT/values/utility_function depending on the type of node. The other properties contain the near_far list which is used by the utility function to determine if a node is a "near to" or "far from" explanation.
 
## History
 
Version 1.0: Initial commit of the finalized code for the project.