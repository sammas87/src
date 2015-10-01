'''
Created on 26.09.2015

@author: schneidersmatthias
'''

import pygame
import Leap
import src.impl.data.handmodel as Handmodel
import math
from src.lib.PGU.pgu import gui

class viewer(gui.Widget):
    def __init__(self,**params):
        #Graphik
        gui.Widget.__init__(self,**params)
        self.showNodes=True
        self.shoEdges=True
        self.width=params['width']
        self.height=params['height']
        self.width2=self.width/2 
        self.height2=self.height/2
        self.bgcolor=(0,0,0)
        pygame.display.set_caption('Handbewegungsanzeiger')
        self.surface=pygame.Surface((self.width,self.height))
        self.surface.fill(self.bgcolor)
#         pygame.display.flip()
        self.nodeColor=(0,0,255)
        self.nodeColor2=(255,0,0)
        self.edgeColor=(215,215,215)
        self.nodeR=4
        ursprung = [[0 for x in range(2)] for x in range(4)]
        ursprung[0][0]=self.width2/2
        ursprung[0][1]=self.height2/2
        ursprung[1][0]=self.width/4*3
        ursprung[1][1]=self.height2/2
        ursprung[2][0]=self.width2/2
        ursprung[2][1]=self.height/4*3
        ursprung[3][0]=self.width/4*3
        ursprung[3][1]=self.height/4*3
        self.ursprungsPunkte=ursprung
        self.offset=[0,0,0]
        self.scaleFactor=1
        self.rot=[0,0,0]
        
    def paint(self,s):
        s.blit(self.surface,(0,0))
        
    def FrameComputation(self,handm):
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key in key_to_function:
                key_to_function[event.key](self)
        #Arm
        handm.addEdge(24,25)
         #Handgelenk
        handm.addEdge(0,24)
        handm.addEdge(4,24)
        handm.addEdge(9,24)
        handm.addEdge(14,24)
        handm.addEdge(19,24)
        #Hand
        handm.addEdge(0,5)
        handm.addEdge(5,10)
        handm.addEdge(10,15)
        handm.addEdge(15,20)
        handm.addEdge(20,19)
        handm.addEdge(19,14)
        handm.addEdge(14,9)
        handm.addEdge(9,4)
        handm.addEdge(4,0)
        handm.addEdge(1,5)        
        #Pinky
        handm.addEdge(20,21)
        handm.addEdge(21,22)
        handm.addEdge(22,23)
        #Ring
        handm.addEdge(15,16)
        handm.addEdge(16,17)
        handm.addEdge(17,18)
        #Middle
        handm.addEdge(10,11)
        handm.addEdge(11,12)
        handm.addEdge(12,13)
        #Index
        handm.addEdge(5,6)
        handm.addEdge(6,7)
        handm.addEdge(7,8) 
        #Thumb
        handm.addEdge(0,1)#i
        handm.addEdge(1,2)
        handm.addEdge(2,3)
        #handm.infoEdges()              
        #doLoop=False
        #drawImage
        self.display(handm)
        self.surface.blit(self.surface,(0,0))
        pygame.display.flip()
        x=5
        x=x+2
        
    

    
    def display(self,handm):
        self.surface.fill(self.bgcolor)
        #zeichne Koordinatensystem
        pygame.draw.aaline(self.surface,(150,150,150),(0,self.height2),(self.width,self.height2))
        pygame.draw.aaline(self.surface,(150,150,150),(self.width2,0),(self.width2,self.height))
        UrsprungSetzenAufWrist=True
        if UrsprungSetzenAufWrist:
            normN=handm.nodes[24]
            for node in handm.nodes:
                node.x=(node.x-normN.x)*self.scaleFactor
                node.y=(node.y-normN.y)*self.scaleFactor
                node.z=(node.z-normN.z)*self.scaleFactor
                node.c=(node.x,node.y,node.z)
                rot=self.rot
                if(not(rot[0]==0)):
                    node=self.rotate(node,0,1,rot[0])
                if(not(rot[1]==0)):
                    node=self.rotate(node,0,2,rot[1])
                if(not(rot[2]==0)):
                    node=self.rotate(node,1,2,rot[2])                 
            #handm.infoNodes()
        for node in handm.nodes:
            c=self.nodeColor2
            if node.exists:
                c=self.nodeColor    
            for dimNr in range(4):
                #pygame.draw.circle(self.surface,(255,0,0),(self.ursprungsPunkte[dimNr][0],self.ursprungsPunkte[dimNr][1]),5)#Einzelkoordinatenursprung
                #zeichne Nodes                
                xoffset,yoffset,x,y,ymult,xmult=self.computeDimensions(dimNr)
                if(dimNr<3):
                    pygame.draw.circle(self.surface, c, (int((node.c[x]*xmult))+xoffset, int((node.c[y]*ymult))+yoffset), self.nodeR)
                #else:
                    #print('To be implemented')
        for edge in handm.edges:
            for dimNr in range(3):
                xoffset,yoffset,x,y,ymult,xmult=self.computeDimensions(dimNr)
                pygame.draw.aaline(self.surface, self.edgeColor, ((edge.begin.c[x]*xmult)+xoffset, (edge.begin.c[y]*ymult)+yoffset), ((edge.end.c[x]*xmult)+xoffset, (edge.end.c[y]*ymult)+yoffset), 1)
        pygame.display.flip()
        
    def rotate(self,node,dim1,dim2,rot):
        coord=node.c
        b=[coord[0],coord[1],coord[2]]
        d=math.hypot(b[dim2], b[dim1])
        w=(math.atan2(b[dim2], b[dim1]))+rot       
        b[dim1]=d*math.cos(w)
        b[dim2]=d*math.sin(w)
        node.x=b[0]
        node.y=b[1]
        node.z=b[2]
        node.c=b
        return node
        
        
    def computeDimensions(self,dimNr):
        xoffset=self.ursprungsPunkte[0][0]
        yoffset=self.ursprungsPunkte[0][1]
        x=2
        y=0
        ymult=-1
        xmult=1
        if(dimNr>0):
            xoffset=self.ursprungsPunkte[dimNr][0]
            yoffset=self.ursprungsPunkte[dimNr][1]
        if(dimNr==1):
            x=0
            y=1
            xmult=-1
        elif(dimNr==2):
            x=2
            y=1
        offset=self.offset
        xoffset=xoffset+offset[x]
        yoffset=yoffset+offset[y]
        #else:
            #print('wie Dimesnion1, to be fixed')
        return xoffset,yoffset,x,y,ymult,xmult
    def translate(self,dimension,aenderung):
        offset=self.offset
        offset[dimension]=offset[dimension]+aenderung
        self.offset=offset
        #if(dimension==0):
        #    self.xoffset=self.xoffset+aenderung
        #elif(dimension==1):
        #    self.yoffset=self.yoffset+aenderung
        #elif(dimension==2):
        #    self.zoffset=self.zoffset+aenderung
    def scale(self,factor):
        self.scaleFactor=factor
        
    def scaleIn(self):
        self.scaleFactor=(self.scaleFactor*1.25)

        
    def scaleOut(self):
        self.scaleFactor=(self.scaleFactor*0.75)
        
    def rotate1(self,dim):
        rot=self.rot
        rot[dim]=rot[dim]+0.1
        self.rot=rot
    def rotate2(self,dim):
        rot=self.rot
        rot[dim]=rot[dim]-0.1
        self.rot=rot
        
    def resetView(self):
        self.scaleFactor=1
        self.offset=[0,0,0]
        self.rot=[0,0,0]
    def ypress(self):
        print('you pressed y')
        
key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translate(0, -10)),
    pygame.K_RIGHT:  (lambda x: x.translate(0,  10)),
    pygame.K_DOWN:   (lambda x: x.translate(1,  10)),
    pygame.K_UP:     (lambda x: x.translate(1, -10)),
    pygame.K_m:   (lambda x: x.translate(2,  10)),
    pygame.K_n:     (lambda x: x.translate(2, -10)),
    pygame.K_q:   (lambda x: x.rotate1(0)),
    pygame.K_w:     (lambda x: x.rotate2(0)),
    pygame.K_e:   (lambda x: x.rotate1(1)),
    pygame.K_r:     (lambda x: x.rotate2(1)),
    pygame.K_s:   (lambda x: x.rotate1(2)),
    pygame.K_d:     (lambda x: x.rotate2(2)),
    pygame.K_0: (lambda x: x.resetView()),
    pygame.K_y: (lambda x: x.ypress()),
    pygame.K_i: (lambda x: x.scaleIn()),
    pygame.K_o:  (lambda x: x.scaleOut()),
    pygame.K_q:  (lambda x:  x.beende2())}