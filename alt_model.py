import sys
import copy
import json
import random
import math
import operator

import numpy as np

def get_node_for_id(i, nodes):
    """
    Gets the node in the network (list of nodes) with the given id (i)
    """
    for n in nodes:
        if n['id'] == i: # finds the matching id
             return n # returns it

def update_network_for_knowledge(net, decisions, knowledge):
    """
    Updates the network (chance nodes) with the knowledge (edges from chance to
    decision)
    """
    for node in net['nodes']:
        if node['type'] == 'decisions':
            for p_id in node['parents']:
                # get parents that are chance nodes and need to be updated
                parent = get_node_for_id(p_id)
                if parent['type'] == 'chance':
                    # update node probability
                    # only works for simple cases now (chance nodes don't have parents)
                    e = [parent['name']+':'+knowledge[parent['name']]]
                    events = []
                    for event in parent['CPT']:
                        if event['event'] != e: # if this isn't the known event
                            events.append(event) # add it to the list
                            events[-1]['prob'] = 0 # with 0 probability
                    parent['CPT'] = [{'event':e, 'prob':1}] # add the known event with prob 1
                    parent['CPT'] += events # add all the events that won't occur
                                            # used for complexity calculations


def row_is_valid(row, decisions):
    """
    Checks if a given row of the CPT matches the decisions
    """
    for e in row['event']:
        if e.split(':')[0] in decisions and decisions[e.split(':')[0]] != e.split(':')[1]:
            return False
    return True

def get_val(name, event):
    """
    Gets the value for a node involved in an event
    """
    for e in event:
        if e.split(':')[0] == name:
            return e.split(':')[1]
    return 'INVALID'

def evaluate_node(node, decisions):
    """
    Evaluates a node
    """
    if node['type'] == 'decision': # if decision node, give it decision value
        node['val'] = decisions[node['name']]
    elif node['type'] == 'chance': # if chance node, randomly select a value
        p = 0
        for row in node['CPT']:
            if row_is_valid(row, decisions):
                p += np.random.random()
                if row['prob'] > p:
                    node['val'] = get_val(node['name'], row['event'])

def calc_utility(net, decisions):
    """
    Calculates the utility for the network
    """
    # find utility node
    utility_node = None
    for node in net['nodes']:
        if node['type'] == 'utility':
            utility_node = node
            break
        else:
            evaluate_node(node, decisions)

    # evaluate utility function
    # This is for the seating experiment, different utility functions can be used here
    # could be part of the network structure
    utility_node['val'] = utility_seating(net, decisions)
    print 'Utility =', utility_node['val']
    return utility_node['val']

def utility_seating(net, decisions):
    """
    Calculates the utility for the seating experiment
    """
    # k is some constant, fit to the data
    # props holds other properties about the network
    k = 0.249
    near_far = net['props']['near_far'] # stores the "near to" or "far from" information

    d = [] # distance list, filled with distance from each person
    r = [] # 
    for node in net['nodes']:
        if node['type'] != 'utility' and node['type'] != 'decision':
            val = int(node['val'])
            d.append([np.abs(val - decisions['seat_choice']), node['name']]) # add distance from each person
    # near_far is an array [0,1] for near, [1,-1] for far
    for i in range(len(d)):
        for j in range(len(near_far)):
            if d[i][1] == near_far[j][2]:
                # e^(-kd) utility
                r.append(near_far[j][0] + near_far[j][1]*np.exp(-k*d[i][0]))
                break
    return np.sum(r)
    

def evaluate_network(net, decisions, knowledge):
    """
    Evaluates the network for utility calculation
    """
    # update network to include knowledge
    update_network_for_knowledge(net, decisions, knowledge)

    # calc utility (rationality check)
    return calc_utility(net, decisions)

def number_of_vals(net, node):
    """
    Calculates the number of values a node can take
    """
    if node['type'] == 'decision':
        return len(node['values']) # if it is a decision node, length of possible values
    elif node['type'] == 'utility':
        # if it is a utility node, the length of 'near_far' is the number of people cared about
        # and it is doubled because you can be near or farm from each of those people
        # and 6 is added because there are 6 places you can sit 
        # (9 total seat - 3 people already there)
        return 6 + 2*len(net['props']['near_far'])
    elif node['type'] == 'chance':
        q = 0
        used = []
        for p in node['CPT']:
            # for each event
            for event in p['event']:
                # check if it has been used before
                if node['name']+':' in event and event not in used:
                    used.append(event)
                    # if not, increase possbile values by 1
                    q += 1
        # constant here to keep network structure files more simple. This is correct becuse
        # there are 9 places for A to sit, 8 for B to sit and 7 for C to sit, 9+8+7 = 24
        # and 8+8+8 = 24
        return 8

def compute_complexity(net):
    """
    Computes the complexity of the network
    """
    # returns a tuple for complexity with and without knowledge edges (knowledge, no_knowledge)
    knowledge = 0 # counting knowledge edges
    no_knowledge = 0 # not counting knowledge edges
    for node in net['nodes']:
        q = 0
        q2 = 0
        for p_id in node['parents']:
            parent = get_node_for_id(p_id, net['nodes'])
            if node['type'] == 'decision' and parent['type'] == 'chance':
                # count knowledge edges seperate
                q2 += number_of_vals(net, parent)
                continue
            q += number_of_vals(net, parent)
        knowledge += (number_of_vals(net, node) - 1) * (q+q2) # q+q2 is all edges
        no_knowledge += (number_of_vals(net, node) - 1) * q # q is all but knowledge edges
    print 'Complexity:',(knowledge, no_knowledge)
    return (knowledge, no_knowledge)


def max_utility(utilities):
    max_val = max(utilities)
    return [1 if abs(u-max_val)<0.02 else 0 for u in utilities]

if __name__ == '__main__':
    spcl = [2,3,4,6,7,8]
    total_knowledge = [] # store all the knowledge prediction values for plotting
    total_complexity = [] # store all complexity values for plotting
    total_utility = [] # store all utility values for plotting
    for ind in [1,2,3,4]: # for each of the 4 cases, load the seat network
        if ind == 1: 
            import seat_networks_x1 as sn
        elif ind == 2:
            import seat_networks_x2 as sn
        elif ind == 3:
            import seat_networks_x3 as sn
        elif ind == 4:
            import seat_networks_x4 as sn
        knowledge = [] # knowledge predictions
        no_knowledge = [] # no knowledge predictions
        complexity = [] # complexity values
        utility = [] # utility values
        
        # Go through all 13 explanations

        case1 = sn.seat_near_a() 
        print 'Case X2, Near A:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        case1 = sn.seat_far_c()
        print 'Case X2, Far C:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_near_a_far_c()
        print 'Case X2, Near A, Far C:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        case1 = sn.seat_near_a_far_b_far_c()
        print 'Case X2, Near A, Far B and C:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_near_a_far_b()
        print 'Case X2, Near A, Far B:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_far_b()
        print 'Case X2, Far B:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_far_b_far_c()
        print 'Case X2, Far B and C:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_far_a()
        print 'Case X2, Far A:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_near_b_far_c()
        print 'Case X2, Near B, Far C:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        complexity.append(c[0])
        utility.append(u)
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_near_a_near_b_far_c()
        print 'Case X2, Near A and B, Far C:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        complexity.append(c[0])
        utility.append(u)
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_near_a_near_b()
        print 'Case X2, Near A and B:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        complexity.append(c[0])
        utility.append(u)
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_near_b()
        print 'Case X2, Near B:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        complexity.append(c[0])
        utility.append(u)
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])
        
        
        case1 = sn.seat_far_a_far_c()
        print 'Case X2, Far A and C:'
        uts = []
        for i in [2,3,4,6,7,8]:
            uts.append(evaluate_network(json.loads(case1[0]), {"seat_choice":i}, json.loads(case1[2])))
        index, value = max(enumerate(uts), key=operator.itemgetter(1))
        u = 0
        if spcl[index] == ind:
            u = 1.0

        c = compute_complexity(json.loads(case1[0]))
        prediction = (u*(1.0/c[0]), u*(1.0/c[1]))
        complexity.append(c[0])
        utility.append(u)
        print 'Prediction:', prediction
        knowledge.append(prediction[0])
        no_knowledge.append(prediction[1])

        # maximizing utility function
        #utility = max_utility(utility)
        knowledge = [utility[c]*(1.0/complexity[c]) for c in range(len(complexity))]

        # print the predicitions, complexity, and utility
        print 'Knowledge Predictions:'
        print json.dumps(knowledge)
        
        print 'No Knowledge Prediction:'
        print json.dumps(no_knowledge)
       
        print 'Complexity:'
        print json.dumps(complexity)

        print 'utility:'
        print json.dumps(utility)
        
        # run the plotting code for this case
        from plot import exp_plot
        exp_plot(np.asarray(knowledge), np.asarray(no_knowledge), np.asarray(complexity, dtype='float64'), np.asarray(utility), ind, 'alt')
        total_knowledge.append(knowledge)
        total_complexity.append(complexity)
        total_utility.append(utility)
    # run the scatter plot code for all the cases
    from plot import exp_full_scatter
    exp_full_scatter(np.asarray(total_knowledge), np.asarray(total_complexity, dtype='float64'), np.asarray(total_utility), 'alt')
