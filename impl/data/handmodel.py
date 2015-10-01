'''
Created on 26.09.2015

@author: schneidersmatthias
'''
class Node:
    def __init__(self,coords,name,exists,isInCoordSys=(True,True,True)):#x,y,z,name,exists):
        #self.x=x
        #self.y=y
        #self.z=z
        self.x=coords[0]
        self.y=coords[1]
        self.z=coords[2]
        self.c=coords
        self.name=name
        self.exists=exists
        self.isInCoordSys=isInCoordSys

class Edge:
    def __init__(self,begin,end):
        self.begin=begin
        self.end=end
class Handmodel:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))

    def addEdges(self, edgeList):
        for (begin,end) in edgeList:
            self.edges.append(Edge(self.nodes[begin], self.nodes[end]))
            
    def addNode(self,node):
        #self.nodes.append(Node(node))
        self.nodes.append(node)
        
    def addEdge(self, begin,end):
        self.edges.append(Edge(self.nodes[begin], self.nodes[end]))

    def infoNodes(self,show=1,timePoint=0):
        result=''
        if(timePoint != 0):
            result="%.5f" % timePoint
        if(show):
            print "\n --- Nodes --- "
        for i, node in enumerate(self.nodes):
            if(show):
                str=" %d: (%.2f, %.2f, %.2f, %s, %s)" % (i, node.x, node.y, node.z, node.name, node.exists)
                print str #" %d: (%.2f, %.2f, %.2f, %s, %s)" % (i, node.x, node.y, node.z, node.name, node.exists)
            str="%d,%.2f,%.2f,%.2f," % (i, node.x, node.y, node.z)
            result=result +str
        result=result+'\n' 
        return result
    
    def infoEdges(self):
        print "\n --- Edges --- "
        for i, edge in enumerate(self.edges):
            print " %d: (%.2f, %.2f, %.2f)" % (i, edge.begin.x, edge.begin.y, edge.begin.z),
            print "to (%.2f, %.2f, %.2f)" % (edge.end.x,  edge.end.y,  edge.end.z)
