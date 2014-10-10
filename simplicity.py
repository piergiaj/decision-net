import sys
import json

def numberOfVals(node):
    q = 0
    used = []
    if node['type'] == 'decision':
        return len(node['values'])
    elif node['type'] == 'utility':
        return len(node['CPT'])
    elif node['type'] == 'chance':
        for p in node['CPT']:
            for event in p['event']:
                if node['name']+':' in event and event not in used:
                    used.append(event)
                    q += 1
    return q


def simplicity(ID):
    val = 0
    eq = ''
    for node in ID['nodes']:
        q = 0
        for p in node['parents']:
            parent = None
            for n in ID['nodes']:
                if n['id'] == p:
                    parent = n
                    break
            if node['type'] == 'decision' and parent['type'] == 'chance': 
                # ignore chance to decision edges
                continue
            q += numberOfVals(parent)
        eq += '('+str(numberOfVals(node))+'-1) * '+str(q)+' + '
        val += (numberOfVals(node)-1)*q
    print eq[:-1]+' = '+str(val)
    return val

def main(i):
    influenceDiagram = json.loads(i)
    return simplicity(influenceDiagram)

def expect(i, e, v):
    if str(e) == str(v):
        print 'Passed '+str(i)
    else:
        print 'Failed '+str(i)+', expected '+str(e)+' got '+str(v)


def test():
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

    i = 1

# net 1
    c = main(net1)
    expect(i, 2, c)
    i += 1

# net 2
    c = main(net2)
    expect(i, 2, c)
    i += 1

# net 3
    c = main(net3)
    expect(i, 12, c)
    i += 1

# net 4
    c = main(net4)
    expect(i, 4, c)
    i += 1

# net 5
    c = main(net5)
    expect(i, 4, c)
    i += 1

# net 6
    c = main(net6)
    expect(i, 2, c)
    i += 1

# net 7
    c = main(net7)
    expect(i, 2, c)
    i += 1

# net 8
    c = main(net8)
    expect(i, 14, c)
    i += 1

# net 9
    c = main(net9)
    expect(i, 12, c)
    i += 1

if __name__ == '__main__':
    if sys.argv[1] == 'test':
        test()
    else:
        print main(sys.argv[1])
