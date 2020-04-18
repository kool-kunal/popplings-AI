import math
from operator import attrgetter
import random

class Activation:
    def __init__(self, a):
        self.a = a
    
    def compute(self, x):
        if self.a == "tanh":
            return math.tanh(x)
        elif self.a == "relu":
            return max(0.0, x) 
        elif self.a == "sigmoid":
            y = 1 + math.e**(-x)
            return 1/y    


class node:
    def __init__(self, t):
        self.id = 0
        self.activation = Activation("tanh")
        self.type = t
        if self.type == "hidden" or self.type == "output":
            self.inputLinks = []
        else:
            self.inputLinks = None
        self.weight = {}
        self.value = None
    
    def out(self, t = None):
        if self.value == None:
            if self.type == "input":
                self.value = self.activation.compute(t*self.weight["-1"])
            else:
                self.value = 0
                for i in self.inputLinks:
                    self.value += self.activation.compute(i.out() * self.weight[i.id])
        
        return self.value
        


class net:
    def __init__(self, inputN, outputN):
        self.nodes = []
        for _ in range(1, inputN + 1):
            self.addNode("input")
        for _ in range(1, outputN + 1):
            self.addNode("output")
        for _ in range(1, 5):
            self.mutate(0.2, 0.4)

    def addNode(self, typeOfNode, inputLink = None, outputLink = None):
        newNode = node(typeOfNode)
        newNode.id = str(len(self.nodes) + 1)
        self.nodes.append(newNode)
        inNode = None
        outNode = None

        if newNode.type == "input":
            newNode.weight.update({"-1": random.uniform(-10, 10)})
            return

        for n in self.nodes:
            if inputLink == n.id:
                inNode = n
            if outputLink == n.id:
                outNode = n

        if inNode != None:
            newNode.inputLinks.append(inNode)
            newNode.weight.update({inNode.id: random.uniform(-10,10)})
        if outNode != None:
            outNode.inputLinks.append(newNode)
            outNode.weight.update({newNode.id: random.uniform(-10,10)})


    def addLink(self, node1, node2):
        if node1 not in node2.inputLinks:
            node2.inputLinks.append(node1)
            node2.weight.update({node1.id: random.uniform(-10, 10)})
        else:
            node2.weight.update({node1.id: random.uniform(-10, 10)})
        

    def output(self, *args):
        input = []
        for a in args:
            input.append(a)
        i=0
        outputV = []
        for n in self.nodes:
            if n.type == "input":
                x = n.out(input[i])
                i += 1
                # print("input " + str(n.id), x)
            elif n.type == "hidden":
                x = n.out()
                # print("hidden " + str(n.id), x)
            else:
                x = n.out()
                outputV.append(x)
                # print("output " + str(n.id), x)

        return outputV

    def mutate(self, addlinkProbability, addNodeProbability):
        al = random.random()
        an = random.random()
        inputNodes = []
        outputNodes = []
        hiddenNodes = []
        for n in self.nodes:
            if n.type == "input":
                inputNodes.append(n)
            elif n.type == "hidden":
                hiddenNodes.append(n)
            elif n.type == "output":
                outputNodes.append(n)

        if al < addlinkProbability:
            nodes = random.choices(hiddenNodes + outputNodes, k=2)
            self.addLink(nodes[0], nodes[1])
        
        if an < addNodeProbability:
            node1 = random.choice(inputNodes + hiddenNodes)

            l = hiddenNodes + outputNodes
            if node1 in l:
                l.remove(node1)
            node2 = random.choice(l)

            self.addNode("hidden", inputLink = node1.id, outputLink = node2.id)


# myNet = net(4, 3)

# for i in range(1, 16):
#     myNet.mutate(0.2, 0.4)
#     # for n in myNet.nodes:
#     #     links = None
#     #     if n.inputLinks != None:
#     #         links = [i.id for i in n.inputLinks]

#     #     print(n.id, n.type, links, n.weight)
#     # print()
         
# outV = myNet.output(1, 2, 3, 4)
# print(outV)