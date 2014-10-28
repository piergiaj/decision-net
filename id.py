import sys
import copy
import json
import random

def numberOfVals(node):
    # finds the number of different values the node can take on
    q = 0
    used = []
    if node['type'] == 'decision':
        # if it is a decision node, simply the length of values
        return len(node['values'])
    elif node['type'] == 'utility':
        # if a utility node, simply rows of table
        return len(node['CPT'])
    elif node['type'] == 'chance':
        # if chance node, find the number of unique values
        for p in node['CPT']:
            # for each event
            for event in p['event']:
                # check if it has been used before
                if node['name']+':' in event and event not in used:
                    used.append(event)
                    # if not, increase possbile values by 1
                    q += 1
    return q

def complexity(ID):
    # calculates complexity according to sum((valsNode-1)*valsParents for all nodes)
    val = 0
    val2 = 0
    eq = ''
    eq2 = ''
    # for each node
    for node in ID['nodes']:
        q = 0
        q2 = 0
        for p in node['parents']:
            parent = getNodeForid(p, ID['nodes'])
            # if the node is a decision and its parent is chance, ignore the edge
            if node['type'] == 'decision' and parent['type'] == 'chance': 
                # ignore chance to decision edges
                q2 += numberOfVals(parent)
                continue
            # get the number of values for this parent
            q += numberOfVals(parent)
        eq += '('+str(numberOfVals(node))+'-1) * '+str(q)+' + '
        eq2 += '('+str(numberOfVals(node))+'-1) * '+str(q+q2)+' + '
        # compute the complexity of this node
        val += (numberOfVals(node)-1)*q
        val2 += (numberOfVals(node)-1)*(q+q2)
    print eq[:-1]+' = '+str(val)
    print eq2[:-1]+' = '+str(val2)
    return (val, val2)


def allDecisions(net):
    # gets list of all possible values of the decisions
    # assumes at most 2 decisions node, complicated if more are added
    decisions = []
    for node in net['nodes']:
        if node['type'] == 'decision':
            decisions.append((node['name'], node['values']))
    allDec = []
    for decision in decisions:
        for v in decision[1]:
            td = {decision[0]: v}
            for d2 in decisions:
                if d2 != decision:
                    for v2 in d2[1]:
                        td2 = copy.deepcopy(td)
                        td2[d2[0]] = v2
                        allDec.append(td2)
                elif len(decisions) == 1:
                    allDec.append(td)
            if len(allDec) == 0:
                allDec.append({decision[0]: v})
    return allDec

def probMaxReward(net, decisions, chanceValues):
    net = json.loads(net)
    decisions = json.loads(decisions)
    chanceValues = json.loads(chanceValues)
    for node in net['nodes']:
        # find utility node to do calculations
        if node['type'] == 'utility':
            pars = parents(node, net, chanceValues, decisions)
            vals = [(row['val'], P(row, pars, decisions, chanceValues, net)) for row in node['CPT']]
            print 'Vals:', vals
            maxReward = max([v[0] for v in vals])
            print 'MaxReward:', maxReward
            r = sum([v[1] for v in vals if v[0] == maxReward])
            print 'P(maxReward | d) =', r
            return r
    

def matchChoice(net, decisions, chanceValues):
    net = json.loads(net)
    all_decisions = allDecisions(net)
    # computes eu for each possible decision
    eus = [calcUtility(json.dumps(net), json.dumps(d), chanceValues, False, False) for d in all_decisions]
    # computes the eu for the given decision
    choiceEU = calcUtility(json.dumps(net), decisions, chanceValues, False, False)

    # return eu(d) / sum(all eus)
    return float(choiceEU[0]) / float(sum([eu[0] for eu in eus]))

def determinedChoice(net, decisions, chanceValues):
    net = json.loads(net)
    all_decisions = allDecisions(net)
    # computes eu for each possible decision
    eus = [calcUtility(json.dumps(net), json.dumps(d), chanceValues, False, False) for d in all_decisions]
    # computes the eu for the given decision
    choiceEU = calcUtility(json.dumps(net), decisions, chanceValues, False, False)
    print '---DETERMINED----'
    print eus
    print choiceEU
    # finds the max value for eu and u
    t = (max([eu[0] for eu in eus]), max([u[1] for u in eus]))
    print t
    # makes sure this decision maximizes eu and u
    # otherwise gives 0 because it is not a good decision
    if not (t[0] <= choiceEU[0]): # should never be less than...
        print '(0, 0) SAD'
        return (0,0)
    # computes 1/ number of good decisions
    t2 = (1.0/[eu[0] for eu in eus].count(t[0]), 1.0/[u[1] for u in eus].count(t[1]))
    print t2
    return t2
    

def parents(n, net, chanceValues, decisions):
    # Assumed that no chance nodes have chance nodes as parents (probably not anymore... I think)
    # What if a chance node has a decision node as a parent and goes to anther decision node?
    possible = []
    for p in n['parents']:
        possible.append(getNodeForid(p, net['nodes']))
    for node in net['nodes']:
        if node['type'] == 'decision':
            for p in node['parents']:
                n = getNodeForid(p, net['nodes'])
                if n in possible:
                   # update the CPT for this node because its value is known and set the 
                    # probability for that event to 1, all other events are not present because
                    # they do not matter
                    parentVals = set()
                    tempPars = []
                    for p2 in n['parents']:
                        n2 = getNodeForid(p2, net['nodes'])
                        tempPars.append(n2)
                        if n2['type'] == 'decision':
                            for r in n2['values']:
                                parentVals.add(r)
                        else:
                            for r in n2['CPT']:
                                for e in r['event']:
                                    if e.split(':')[0] == n2['name']:
                                        parentVals.add(e)
                    tmpDct = dict(chanceValues.items() + decisions.items())
                    if len(parentVals) == 0:
                        tmpcpt = []
                        for e in n['CPT']:
                            if e['event'][0] != n['name']+':'+chanceValues[n['name']]:
                                tmpcpt.append({'event':e['event'], 'prob':0})
                        n['CPT'] = tmpcpt
                        n['CPT'].append({'event':[n['name']+':'+chanceValues[n['name']]], 'prob': 1})
                    else:
                        tmpcpt = []
                        for e in n['CPT']:
                            if n['name']+':'+tmpDct[n['name']] not in e['event'] and tempPars[0]['name']+':'+tmpDct[tempPars[0]['name']] not in e['event']:
                                tmpcpt.append({'event':e['event'], 'prob':0})
                        n['CPT'].append({'event':[tempPars[0]['name']+':'+tmpDct[tempPars[0]['name']], n['name']+':'+tmpDct[n['name']]], 'prob': 1})
    return possible

def P_row(node, row, parents, decisions):
    val = 1
    for e in row['event']:
        name = e.split(':')
        if name[0] == node['name']:
            continue
        for p in parents:
            if p['name'] == name[0]:
                for ev in p['CPT']:
                    if e in ev['event']:
                        val *= ev['prob']
    return val
def P(row, nodes, decisions, chanceValues, net):
    val = 1
    for e in row['event']: # go through each row
        name = e.split(':')[0]
        v = e.split(':')[1]
        for n in nodes: 
            if n['name'] == name and n['type'] == 'chance': # find the node for this event
                for x in n['CPT']: # for each possible value of this node
                    valid = True
                    for y in x['event']: # check if this one is what we are looking for
                        if e != y: # if it doesn't match
                            decisionCheck = False
                            for d in decisions: # and it isn't the decision
                                if y != d+':'+decisions[d]:
                                    valid = False # it is not what we are looking for
                                else:
                                    decisionCheck = True
                            if not valid and decisionCheck:
                                valid = True
                    if valid: # it is what we are looking for
                        val *= x['prob'] # multiply prob
            elif n['name'] == name and n['type'] == 'decision': # found decision node
                if v != decisions[name]: # if this decision is not the decision for this row
                    val = 0 # this row is invalid and has 0 value
    return val

def expectedUtility(net, decisions, chanceValues, debug=False):
    eu = 0
    debugString = ''
    for node in net['nodes']:
        if node['type'] == 'utility':
            pars = parents(node, net, chanceValues, decisions)
            for row in node['CPT']:
                valid = True
                for tv in row['event']:
                    if tv.split(':')[0] in decisions and decisions[tv.split(':')[0]] != tv.split(':')[1]:
                        valid = False
                if not valid:
                    continue
                summation = 0
                for p in pars:
                    if p['type'] == 'decision':
                        if len(pars) == 1:
                            summation += 1
                        continue
                    pars2 = parents(p, net, chanceValues, decisions)
                    tmp = [v for v in row['event'] if v.split(':')[0] == p['name']][0]
                    for r2 in p['CPT']:
                        valid = True
                        for tv in r2['event']:
                            if tv.split(':')[0] in decisions and decisions[tv.split(':')[0]] != tv.split(':')[1]:
                                valid = False
                        if not valid:
                            continue
                        if tmp in r2['event']:
                            prod = 1
                            for p2 in pars2:
                                if p2['type'] == 'decision':
                                    continue
                                #print p2['name'], r2['event'], p['name']#, p['CPT']
                                tmp2 = [v for v in r2['event'] if v.split(':')[0] == p2['name']][0]
                                #print p2['CPT']
                                for r3 in p2['CPT']:
                                    isValid = True
                                    for tmpEvent in r3['event']:
                                        if tmpEvent.split(':')[0] in decisions and decisions[tmpEvent.split(':')[0]] != tmpEvent.split(':')[1]:
                                            isValid = False
                                    if tmp2 in r3['event'] and isValid:
                                        prod *= r3['prob']
                                        debugString += ' prod * '+str(r3['prob'])+'  '+str(r3['event'])+'\n'
                            summation += r2['prob'] * prod
                            debugString += ' + '+str(r2['prob'])+' * '+str(prod)
                            debugString += ' = '+str(r2['prob']*prod)+'\n'
                debugString += 'eu += '+str(summation)+' * '+str(row['val'])+' = '+str(summation*row['val'])+'\n'
                eu += summation*row['val']
                debugString += 'EU = '+str(eu)+'\n'
    if debug:
        print debugString
    return eu
                                    
                        
def expectedUtility2(net, decisions, chanceValues, prnt=True):
    # assumes no chance nodes have chance nodes as parents, so all nodes have simple CPTs
    eu = 0
    for node in net['nodes']:
        # finds the utility node
        if node['type'] == 'utility':
          # gets the parent of the utility node and updates values of known chance nodes
          par = parents(node, net, chanceValues)
          for row in node['CPT']:
              # for each for in the utility function
              if prnt:
                  print str(row)+' * '+str(P(row,par,decisions,chanceValues,net))+' = '+str(row['val'] * P(row, par, decisions, chanceValues, net))
              # calculate the probability of it occuring and add it to eu
              eu += row['val'] * P(row, par, decisions, chanceValues, net)
    if prnt:
        print 'EU('+str(decisions)+') = '+str(eu)                  
    return eu

def getNodeForid(i, nodes):
    for n in nodes:
        if n['id'] == i:
             return n

def evaluateNode(node, nodes, decisions, chanceValues):
    # finds the value of this node
    if 'val' in node:
        # don't evaluate already evaluated nodes
        return node['val']
    for p in node['parents']:
        # evaluate all its parents
        evaluateNode(getNodeForid(p,nodes), nodes, decisions, chanceValues)
    if node['type'] == 'chance':
        # if it is a chance node, give it the given value
        node['val'] = chanceValues[node['name']]
    elif node['type'] == 'decision':
        # if it is a decision node, give the decision value
        node['val'] = decisions[node['name']]
        return
    elif node['type'] == 'utility':
        # don't evaluate utilty here
        pass
    cpt = []
                                        
    for p in node['parents']:
        # for each parent
        parent = getNodeForid(p,nodes)
        # build the full cptnn
        cpt.append(parent['name']+':'+parent['val'])
        # for each possible CPT entry
        for possible in node['CPT']:
            # check if it matches this cpt
            if sorted(cpt) == sorted(possible['event']):
                # if so, assign this node the given value
                node['val'] = possible['val']
                return possible['val']
                        


def calcUtility(i,d,c,v=False, prnt=True):
    influenceDiagram = json.loads(i)
    decisions = json.loads(d)
    chanceValues = json.loads(c)
    print decisions, chanceValues
    # evaluate all nodes, including the utility node
    for node in influenceDiagram['nodes']:
        evaluateNode(node, influenceDiagram['nodes'], decisions, chanceValues)
    if v:
        print influenceDiagram
        print 'Evaluated Network:'
        print [str(n['name'])+':'+str(n['val']) for n in influenceDiagram['nodes']]
        print 'Expected Utility:'
    u = None
    for n in influenceDiagram['nodes']:
        if n['type'] == 'utility':
            if 'val' not in n:
                evaluateNode(n, influenceDiagram['nodes'], decisions, chanceValues)
            print decisions, chanceValues
            u = n['val']
    # compute eu
    eu = expectedUtility(influenceDiagram, decisions, chanceValues, prnt)
    print 'The utility is', eu
    #eu2 = expectedUtility2(influenceDiagram, decisions, chanceValues, prnt)
    if v:
        print eu
        print 'EU2 =', eu2
    return (eu,u)

def expect(i, e, v):
    if isinstance(e, tuple) and abs(e[0] - v[0]) < 0.001 and abs(e[1]-v[1]) < 0.001:
        print '\033[92m'+'Passed '+str(i)+'\033[0m'
    elif (not isinstance(e, tuple)) and abs(e-v) < 0.001:
        print '\033[92m'+'Passed '+str(i)+'\033[0m'
    else:
        print '\033[91m' + 'Failed '+str(i)+', expected '+str(e)+' got '+str(v)+'\033[0m'

def test():
    decisionTrue = '{"d":"T"}'
    decisionFalse = '{"d":"F"}'
    chanceTrue = '{"c":"T"}'
    chanceFalse = '{"c":"F"}'

    net1 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["c:T"],"prob":0.6},{"event":["c:F"],"prob":0.4}],"parents":[]},{"id":1,"type":"decision","name":"d","parents":[],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["c:T"],"val":0},{"event":["c:F"],"val":1}],"parents":[0]}]}'
    net2 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["c:T"],"prob":0.6},{"event":["c:F"],"prob":0.4}],"parents":[]},{"id":1,"type":"decision","name":"d","parents":[],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["d:T"],"val":0},{"event":["d:F"],"val":1}],"parents":[1]}]}'
    net3 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["c:T"],"prob":0.6},{"event":["c:F"],"prob":0.4}],"parents":[]},{"id":1,"type":"decision","name":"d","parents":[],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["c:T","d:T"],"val":1},{"event":["c:T","d:F"],"val":0},{"event":["c:F","d:T"],"val":0},{"event":["c:F","d:F"],"val":1}],"parents":[0,1]}]}'
    net4 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["d:T","c:T"],"prob":0.3},{"event":["d:T","c:F"],"prob":0.7},{"event":["d:F","c:T"],"prob":0.4},{"event":["d:F","c:F"],"prob":0.6}],"parents":[1]},{"id":1,"type":"decision","name":"d","parents":[],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["c:T"],"val":1},{"event":["c:F"],"val":0}],"parents":[0]}]}'
    net5 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["d:T","c:T"],"prob":0.8},{"event":["d:T","c:F"],"prob":0.2},{"event":["d:F","c:T"],"prob":0.6},{"event":["d:F","c:F"],"prob":0.4}],"parents":[1]},{"id":1,"type":"decision","name":"d","parents":[],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["d:T"],"val":0},{"event":["d:F"],"val":1}],"parents":[1]}]}'
    net6 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["c:T"],"prob":0.7},{"event":["c:F"],"prob":0.3}],"parents":[]},{"id":1,"type":"decision","name":"d","parents":[0],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["d:T"],"val":0},{"event":["d:F"],"val":1}],"parents":[1]}]}'
    net7 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["c:T"],"prob":0.6},{"event":["c:F"],"prob":0.4}],"parents":[]},{"id":1,"type":"decision","name":"d","parents":[0],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["c:T"],"val":1},{"event":["c:F"],"val":0}],"parents":[0]}]}'
    net8 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["d:T","c:T"],"prob":0.7},{"event":["d:T","c:F"],"prob":0.3},{"event":["d:F","c:T"],"prob":0.4},{"event":["d:F","c:F"],"prob":0.6}],"parents":[1]},{"id":1,"type":"decision","name":"d","parents":[],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["c:T","d:T"],"val":1},{"event":["c:T","d:F"],"val":0},{"event":["c:F","d:T"],"val":0},{"event":["c:F","d:F"],"val":1}],"parents":[0,1]}]}'
    net9 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["c:T"],"prob":0.6},{"event":["c:F"],"prob":0.4}],"parents":[]},{"id":1,"type":"decision","name":"d","parents":[0],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["c:T","d:T"],"val":1},{"event":["c:T","d:F"],"val":0},{"event":["c:F","d:T"],"val":0},{"event":["c:F","d:F"],"val":1}],"parents":[0,1]}]}'
    net10 = '{"nodes":[{"id":0,"type":"chance","name":"c","CPT":[{"event":["d:T","c:T"],"prob":0.6},{"event":["d:T","c:F"],"prob":0.4},{"event":["d:F","c:T"],"prob":0.7},{"event":["d:F","c:F"],"prob":0.3}],"parents":[1]},{"id":1,"type":"decision","name":"d","parents":[],"values":["T","F"]},{"id":2,"type":"utility","name":"u","CPT":[{"event":["d:T","c:T"],"val":2},{"event":["d:T","c:F"],"val":3},{"event":["d:F","c:T"],"val":2},{"event":["d:F","c:F"],"val":4}],"parents":[1,0]}]}'

    net11 = '{"nodes":[{"id":0,"type":"chance","name":"roll","CPT":[{"event":["dice:A","roll:R"],"prob":0.6},{"event":["dice:A","roll:G"],"prob":0.2},{"event":["dice:A","roll:Y"],"prob":0.2},{"event":["dice:B","roll:R"],"prob":0.5},{"event":["dice:B","roll:G"],"prob":0.4},{"event":["dice:B","roll:Y"],"prob":0.1},{"event":["dice:C","roll:R"],"prob":0.2},{"event":["dice:C","roll:G"],"prob":0.3},{"event":["dice:C","roll:Y"],"prob":0.5}],"parents":[1]},{"id":1,"type":"decision","name":"dice","parents":[],"values":["A","B","C"]},{"id":2,"type":"decision","name":"color","parents":[],"values":["R","G","Y"]},{"id":3,"type":"utility","name":"u","CPT":[{"event":["roll:R","dice:A","color:R"],"val":1},{"event":["roll:R","dice:A","color:G"],"val":0},{"event":["roll:R","dice:A","color:Y"],"val":0},{"event":["roll:R","dice:B","color:R"],"val":1},{"event":["roll:R","dice:B","color:G"],"val":0},{"event":["roll:R","dice:B","color:Y"],"val":0},{"event":["roll:R","dice:C","color:R"],"val":1},{"event":["roll:R","dice:C","color:G"],"val":0},{"event":["roll:R","dice:C","color:Y"],"val":0},{"event":["roll:G","dice:A","color:R"],"val":0},{"event":["roll:G","dice:A","color:G"],"val":1},{"event":["roll:G","dice:A","color:Y"],"val":0},{"event":["roll:G","dice:B","color:R"],"val":0},{"event":["roll:G","dice:B","color:G"],"val":1},{"event":["roll:G","dice:B","color:Y"],"val":0},{"event":["roll:G","dice:C","color:R"],"val":0},{"event":["roll:G","dice:C","color:G"],"val":1},{"event":["roll:G","dice:C","color:Y"],"val":0},{"event":["roll:Y","dice:A","color:R"],"val":0},{"event":["roll:Y","dice:A","color:G"],"val":0},{"event":["roll:Y","dice:A","color:Y"],"val":1},{"event":["roll:Y","dice:B","color:R"],"val":0},{"event":["roll:Y","dice:B","color:G"],"val":0},{"event":["roll:Y","dice:B","color:Y"],"val":1},{"event":["roll:Y","dice:C","color:R"],"val":0},{"event":["roll:Y","dice:C","color:G"],"val":0},{"event":["roll:Y","dice:C","color:Y"],"val":1}],"parents":[0,1,2]}]}'
    net12 = '{"nodes":[{"id":0,"type":"chance","name":"dice","CPT":[{"event":["dice:A"],"prob":0.33},{"event":["dice:B"],"prob":0.33},{"event":["dice:C"],"prob":0.34}],"parents":[]},{"id":1,"type":"chance","name":"roll","CPT":[{"event":["dice:A","roll:r"],"prob":0.5},{"event":["dice:A","roll:b"],"prob":0.5},{"event":["dice:B","roll:r"],"prob":0.7},{"event":["dice:B","roll:b"],"prob":0.3},{"event":["dice:C","roll:r"],"prob":0.9},{"event":["dice:C","roll:b"],"prob":0.1}],"parents":[0]},{"id":2,"type":"decision","name":"d","parents":[],"values":["r","b"]},{"id":3,"type":"utility","name":"u","CPT":[{"event":["roll:r","d:r"],"val":1},{"event":["roll:r","d:b"],"val":0},{"event":["roll:b","d:r"],"val":0},{"event":["roll:b","d:b"],"val":1}],"parents":[1,2]}]}'
    
    def testUtility():
        i = 1

        # net 1
        eu = calcUtility(net1, decisionTrue, chanceTrue, False)
        expect(i, (0.4,0), eu)
        i += 1

        eu = calcUtility(net1, decisionTrue, chanceFalse, False)
        expect(i, (0.4,1), eu)
        i += 1

        eu = calcUtility(net1, decisionFalse, chanceTrue, False)
        expect(i, (0.4,0), eu)
        i += 1
        
        eu = calcUtility(net1, decisionFalse, chanceFalse, False)
        expect(i, (0.4, 1), eu)
        i += 1
        
        # net 2
        eu = calcUtility(net2, decisionTrue, chanceTrue, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net2, decisionTrue, chanceFalse, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net2, decisionFalse, chanceTrue, False)
        expect(i, (1,1), eu)
        i += 1
        
        eu = calcUtility(net2, decisionFalse, chanceFalse, False)
        expect(i, (1,1), eu)
        i += 1
        
        # net 3
        eu = calcUtility(net3, decisionTrue, chanceTrue, False)
        expect(i, (0.6,1), eu)
        i += 1
        
        eu = calcUtility(net3, decisionTrue, chanceFalse, False)
        expect(i, (0.6,0), eu)
        i += 1
        
        eu = calcUtility(net3, decisionFalse, chanceTrue, False)
        expect(i, (0.4,0), eu)
        i += 1
        
        eu = calcUtility(net3, decisionFalse, chanceFalse, False)
        expect(i, (0.4,1), eu)
        i += 1
        
        # net 4
        eu = calcUtility(net4, decisionTrue, chanceTrue, False)
        expect(i, (0.3,1), eu)
        i += 1
        
        eu = calcUtility(net4, decisionTrue, chanceFalse, False)
        expect(i, (0.3,0), eu)
        i += 1
        
        eu = calcUtility(net4, decisionFalse, chanceTrue, False)
        expect(i, (0.4,1), eu)
        i += 1
        
        eu = calcUtility(net4, decisionFalse, chanceFalse, False)
        expect(i, (0.4,0), eu)
        i += 1
        
        # net 5
        eu = calcUtility(net5, decisionTrue, chanceTrue, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net5, decisionTrue, chanceFalse, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net5, decisionFalse, chanceTrue, False)
        expect(i, (1,1), eu)
        i += 1
        
        eu = calcUtility(net5, decisionFalse, chanceFalse, False)
        expect(i, (1,1), eu)
        i += 1
        
        # net 6
        eu = calcUtility(net6, decisionTrue, chanceTrue, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net6, decisionTrue, chanceFalse, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net6, decisionFalse, chanceTrue, False)
        expect(i, (1,1), eu)
        i += 1
        
        eu = calcUtility(net6, decisionFalse, chanceFalse, False)
        expect(i, (1,1), eu)
        i += 1
        
        # net 7
        eu = calcUtility(net7, decisionTrue, chanceTrue, False)
        expect(i, (1,1), eu)
        i += 1
        
        eu = calcUtility(net7, decisionTrue, chanceFalse, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net7, decisionFalse, chanceTrue, False)
        expect(i, (1,1), eu)
        i += 1
        
        eu = calcUtility(net7, decisionFalse, chanceFalse, False)
        expect(i, (0,0), eu)
        i += 1
        
        # net 8
        eu = calcUtility(net8, decisionTrue, chanceTrue, False)
        expect(i, (0.7,1), eu)
        i += 1
        
        eu = calcUtility(net8, decisionTrue, chanceFalse, False)
        expect(i, (0.7,0), eu)
        i += 1
        
        eu = calcUtility(net8, decisionFalse, chanceTrue, False)
        expect(i, (0.6,0), eu)
        i += 1
        
        eu = calcUtility(net8, decisionFalse, chanceFalse, False)
        expect(i, (0.6,1), eu)
        i += 1
        
        # net 9
        eu = calcUtility(net9, decisionTrue, chanceTrue, False)
        expect(i, (1,1), eu)
        i += 1
        
        eu = calcUtility(net9, decisionTrue, chanceFalse, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net9, decisionFalse, chanceTrue, False)
        expect(i, (0,0), eu)
        i += 1
        
        eu = calcUtility(net9, decisionFalse, chanceFalse, False)
        expect(i, (1,1), eu)
        i += 1
        
        # net 10
        eu = calcUtility(net10, decisionTrue, chanceTrue, False)
        expect(i, (2.4,2), eu)
        i += 1
        
        eu = calcUtility(net10, decisionTrue, chanceFalse, False)
        expect(i, (2.4,3), eu)
        i += 1
        
        eu = calcUtility(net10, decisionFalse, chanceTrue, False)
        expect(i, (2.6,2), eu)
        i += 1
        
        eu = calcUtility(net10, decisionFalse, chanceFalse, False)
        expect(i, (2.6,4), eu)
        i += 1

        # net 11
        eu = calcUtility(net11, '{"dice":"A", "color":"R"}', '{"roll":"R"}', False)
        expect(i, (0.6, 1), eu)

    
    def testDetermined():
        i = 1

        # net 1
        val = determinedChoice(net1, decisionTrue, chanceTrue)
        expect(i, (0.5, 0.5), val)
        i += 1

        val = determinedChoice(net1, decisionTrue, chanceFalse)
        expect(i, (0.5, 0.5), val)
        i += 1

        val = determinedChoice(net1, decisionFalse, chanceTrue)
        expect(i, (0.5, 0.5), val)
        i += 1

        val = determinedChoice(net1, decisionFalse, chanceFalse)
        expect(i, (0.5, 0.5), val)
        i += 1

        # net 2
        val = determinedChoice(net2, decisionTrue, chanceTrue)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net2, decisionTrue, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net2, decisionFalse, chanceTrue)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net2, decisionFalse, chanceFalse)
        expect(i, (1, 1), val)
        i += 1

        # net 3
        val = determinedChoice(net3, decisionTrue, chanceTrue)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net3, decisionTrue, chanceFalse)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net3, decisionFalse, chanceTrue)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net3, decisionFalse, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        # net 4
        val = determinedChoice(net4, decisionTrue, chanceTrue)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net4, decisionTrue, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net4, decisionFalse, chanceTrue)
        expect(i, (1, 0.5), val)
        i += 1

        val = determinedChoice(net4, decisionFalse, chanceFalse)
        expect(i, (1, 0.5), val)
        i += 1

        # net 5
        val = determinedChoice(net5, decisionTrue, chanceTrue)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net5, decisionTrue, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net5, decisionFalse, chanceTrue)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net5, decisionFalse, chanceFalse)
        expect(i, (1, 1), val)
        i += 1

        # net 6
        val = determinedChoice(net6, decisionTrue, chanceTrue)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net6, decisionTrue, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net6, decisionFalse, chanceTrue)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net6, decisionFalse, chanceFalse)
        expect(i, (1, 1), val)
        i += 1

        # net 7
        val = determinedChoice(net7, decisionTrue, chanceTrue)
        expect(i, (0.5, 0.5), val)
        i += 1

        val = determinedChoice(net7, decisionTrue, chanceFalse)
        expect(i, (0.5, 0.5), val)
        i += 1

        val = determinedChoice(net7, decisionFalse, chanceTrue)
        expect(i, (0.5, 0.5), val)
        i += 1

        val = determinedChoice(net7, decisionFalse, chanceFalse)
        expect(i, (0.5, 0.5), val)
        i += 1

        # net 8
        val = determinedChoice(net8, decisionTrue, chanceTrue)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net8, decisionTrue, chanceFalse)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net8, decisionFalse, chanceTrue)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net8, decisionFalse, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        # net 9
        val = determinedChoice(net9, decisionTrue, chanceTrue)
        expect(i, (1, 1), val)
        i += 1

        val = determinedChoice(net9, decisionTrue, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net9, decisionFalse, chanceTrue)
        expect(i, (0,0), val)
        i += 1

        val = determinedChoice(net9, decisionFalse, chanceFalse)
        expect(i, (1, 1), val)
        i += 1

        # net 10
        val = determinedChoice(net10, decisionTrue, chanceTrue)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net10, decisionTrue, chanceFalse)
        expect(i, (0, 0), val)
        i += 1

        val = determinedChoice(net10, decisionFalse, chanceTrue)
        expect(i, (1, 0.5), val)
        i += 1

        val = determinedChoice(net10, decisionFalse, chanceFalse)
        expect(i, (1, 1), val)
        i += 1

        # net 11
        val = determinedChoice(net11, '{"dice":"A", "color":"G"}', '{"roll":"R"}')

    def testComplexity():
        i = 1

        # net 1
        c = complexity(json.loads(net1))
        expect(i, 2, c)
        i += 1
        
        # net 2
        c = complexity(json.loads(net2))
        expect(i, 2, c)
        i += 1
        
        # net 3
        c = complexity(json.loads(net3))
        expect(i, 12, c)
        i += 1
        
        # net 4
        c = complexity(json.loads(net4))
        expect(i, 4, c)
        i += 1
        
        # net 5
        c = complexity(json.loads(net5))
        expect(i, 4, c)
        i += 1
        
        # net 6
        c = complexity(json.loads(net6))
        expect(i, 2, c)
        i += 1
        
        # net 7
        c = complexity(json.loads(net7))
        expect(i, 2, c)
        i += 1

        # net 8
        c = complexity(json.loads(net8))
        expect(i, 14, c)
        i += 1

        # net 9
        c = complexity(json.loads(net9))
        expect(i, 12, c)
        i += 1

    def testMaxProb():
        i = 1

        # net 1
        p = probMaxReward(net1, decisionTrue, chanceTrue)
        expect(i, 0.4, p)
        i += 1

        p = probMaxReward(net1, decisionTrue, chanceFalse)
        expect(i, 0.4, p)
        i += 1

        p = probMaxReward(net1, decisionFalse, chanceTrue)
        expect(i, 0.4, p)
        i += 1

        p = probMaxReward(net1, decisionFalse, chanceFalse)
        expect(i, 0.4, p)
        i += 1

        # net 2
        p = probMaxReward(net2, decisionTrue, chanceTrue)
        expect(i, 0, p)
        i += 1

        p = probMaxReward(net2, decisionTrue, chanceFalse)
        expect(i, 0, p)
        i += 1

        p = probMaxReward(net2, decisionFalse, chanceTrue)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net2, decisionFalse, chanceFalse)
        expect(i, 1, p)
        i += 1

        # net 3
        p = probMaxReward(net3, decisionTrue, chanceTrue)
        expect(i, 0.6, p)
        i += 1

        p = probMaxReward(net3, decisionTrue, chanceFalse)
        expect(i, 0.6, p)
        i += 1

        p = probMaxReward(net3, decisionFalse, chanceTrue)
        expect(i, 0.4, p)
        i += 1

        p = probMaxReward(net3, decisionFalse, chanceFalse)
        expect(i, 0.4, p)
        i += 1

        # net 4
        p = probMaxReward(net4, decisionTrue, chanceTrue)
        expect(i, 0.3, p)
        i += 1

        p = probMaxReward(net4, decisionTrue, chanceFalse)
        expect(i, 0.3, p)
        i += 1

        p = probMaxReward(net4, decisionFalse, chanceTrue)
        expect(i, 0.4, p)
        i += 1

        p = probMaxReward(net4, decisionFalse, chanceFalse)
        expect(i, 0.4, p)
        i += 1

        # net 5
        p = probMaxReward(net5, decisionTrue, chanceTrue)
        expect(i, 0, p)
        i += 1

        p = probMaxReward(net5, decisionTrue, chanceFalse)
        expect(i, 0, p)
        i += 1

        p = probMaxReward(net5, decisionFalse, chanceTrue)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net5, decisionFalse, chanceFalse)
        expect(i, 1, p)
        i += 1

        # net 6
        p = probMaxReward(net6, decisionTrue, chanceTrue)
        expect(i, 0, p)
        i += 1

        p = probMaxReward(net6, decisionTrue, chanceFalse)
        expect(i, 0, p)
        i += 1

        p = probMaxReward(net6, decisionFalse, chanceTrue)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net6, decisionFalse, chanceFalse)
        expect(i, 1, p)
        i += 1

        # net 7
        p = probMaxReward(net7, decisionTrue, chanceTrue)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net7, decisionTrue, chanceFalse)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net7, decisionFalse, chanceTrue)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net7, decisionFalse, chanceFalse)
        expect(i, 1, p)
        i += 1

        # net 8
        p = probMaxReward(net8, decisionTrue, chanceTrue)
        expect(i, 0.7, p)
        i += 1

        p = probMaxReward(net8, decisionTrue, chanceFalse)
        expect(i, 0.7, p)
        i += 1

        p = probMaxReward(net8, decisionFalse, chanceTrue)
        expect(i, 0.6, p)
        i += 1

        p = probMaxReward(net8, decisionFalse, chanceFalse)
        expect(i, 0.6, p)
        i += 1

        # net 9
        p = probMaxReward(net9, decisionTrue, chanceTrue)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net9, decisionTrue, chanceFalse)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net9, decisionFalse, chanceTrue)
        expect(i, 1, p)
        i += 1

        p = probMaxReward(net9, decisionFalse, chanceFalse)
        expect(i, 1, p)
        i += 1

    
    return (testUtility, testDetermined, testComplexity, testMaxProb)


if __name__ == '__main__':
    tst = test()
    if sys.argv[1] == 'testUtility':
        tst[0]()
    elif sys.argv[1] == 'testDetermined':
        tst[1]()
    elif sys.argv[1] == 'testComplexity':
        tst[2]()
    elif sys.argv[1] == 'testMaxProb':
        tst[3]()
    elif sys.argv[1] == 'calcComplexity':
        print complexity(json.loads(sys.argv[2]))
    else:
        us = calcUtility(sys.argv[1], sys.argv[2], sys.argv[3])
        det = determinedChoice(sys.argv[1], sys.argv[2], sys.argv[3])
        complexity = complexity(json.loads(sys.argv[1]))
        pMax = probMaxReward(sys.argv[1], sys.argv[2], sys.argv[3])
        mchoice = matchChoice(sys.argv[1], sys.argv[2], sys.argv[3])

        print ' '
        print '(EU, U) =', us
        print 'Determined:', det
        print 'Complexity:', complexity
        print 'P(maxReward | d) =', pMax
        print 'P(proportional_choice | net) =', mchoice
        
        print ' ' 
        print 'P1'
        print 'P(max_choice | net) * P(net_no_knowedge) ='
        print det[0], '* 1 /', complexity[0], '=', det[0], '*', 1.0/complexity[0], '=', det[0]*(1.0/complexity[0])
        
        print 'P2'
        print 'P(max_choice | net) * P(net_knowledge) ='
        print det[0], '* 1 /', complexity[1], '=', det[0], '*', 1.0/complexity[1], '=', det[0]*(1.0/complexity[1])

        print 'P3'
        print 'P(proportional_choice | net) * P(net_no_knowledge) ='
        print mchoice, '* 1 /', complexity[0], '=', mchoice, '*', 1.0/complexity[0], '=', mchoice*(1.0/complexity[0])
        
        print 'P4'
        print 'P(proportional_choice | net) * P(net_knowedge) ='
        print mchoice, '* 1 /', complexity[1], '=', mchoice, '*', 1.0/complexity[1], '=', mchoice*(1.0/complexity[1])
