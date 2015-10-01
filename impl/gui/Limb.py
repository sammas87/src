# -*- coding: iso-8859-15 -*-
'''
Created on 13.09.2015

@author: schneidersmatthias
'''

import numpy as np
import pygame
import math
from src.lib.PGU.pgu import gui

class UpperLimb(gui.Widget):
        def __init__(self,**params):
            gui.Widget.__init__(self,**params)
            self.width=params['width']
            self.width2=math.floor(self.width/2)
            self.width2Offset=5
            self.width2=self.width2-self.width2Offset
            self.height=params['height']
            self.surface = pygame.Surface((self.width,self.height))
            self.surface.fill((0,0,0))            
            self.PointsHand=np.array([[0.34269,0.99244],[0.18819,0.88644],[0.16895,0.84661],[0.1421,0.7881],[0.11407,0.75216],[0.074068,0.68342],[0,0.62893],[0.0044214,0.5936],[0.046385,0.57564],[0.084764,0.57653],[0.11137,0.58208],[0.17131,0.61973],[0.2023,0.67088],[0.22103,0.69738],[0.24765,0.71296],[0.27508,0.71509],[0.29942,0.70334],[0.31735,0.67291],[0.33171,0.61573],[0.33202,0.56231],[0.31087,0.43174],[0.26848,0.15367],[0.28083,0.1239],[0.30512,0.11084],[0.34009,0.11402],[0.36339,0.13195],[0.37067,0.16862],[0.43928,0.44474],[0.45834,0.4735],[0.47153,0.46488],[0.48022,0.4304],[0.51257,0.14118],[0.51817,0.062913],[0.53059,0.02381],[0.54513,0.0081153],[0.57923,0],[0.59569,0.011145],[0.60744,0.026114],[0.61839,0.062069],[0.61981,0.091097],[0.61778,0.14472],[0.6059,0.40519],[0.60904,0.47357],[0.62299,0.49138],[0.63286,0.4751],[0.65221,0.39662],[0.71195,0.17605],[0.74114,0.13189],[0.76835,0.12234],[0.79152,0.12657],[0.80525,0.14146],[0.80878,0.15412],[0.80844,0.17349],[0.77559,0.41214],[0.74813,0.57369],[0.85283,0.47672],[0.91692,0.39001],[0.95974,0.35499],[0.98268,0.36234],[0.99083,0.36953],[0.99624,0.37849],[0.99924,0.38905],[1,0.40065],[0.98858,0.44583],[0.96688,0.4805],[0.86502,0.62525],[0.83256,0.71126],[0.80821,0.85408],[0.77572,0.99236]] )
            self.PointsArm=np.array([[0.77572,0],[0.79572,0.33332],[0.85072,0.59997],[0.86572,0.7333],[0.85072,0.86662],[0.82572,0.99995],[0.31269,1],[0.28269,0.93334],[0.26769,0.83334],[0.32269,0.50003],[0.34269,5.1461e-005]] )
            self.handUsed=None
            self.handTopViewPoints=None
            self.handLowerViewPoints=None
            self.armUsed=None
            self.repaint()
        
        #limbSide ExtlowerArmLengthcm limbWristPerimetercm
        def computeUpperLimb(self,wristWidth,ExtlowerArmLengthcm,handlength,limbSide,reDraw):
            reDraw=reDraw()
            if(reDraw):
                ExtlowerArmLengthcm=ExtlowerArmLengthcm()
                handlength=handlength()
                limbSide=limbSide()
                wristWidth=wristWidth()
                #handlength can be guessed by limbWristPerimetercm
                hand=self.PointsHand.copy()
                arm=self.PointsArm.copy()
                hand[:,1]=hand[:,1]*handlength
                arm[:,1]=arm[:,1]*ExtlowerArmLengthcm+handlength 
                actHandWidth=hand[0,0]-hand[hand.shape[0]-1,0]
                
                       
                self.armUsed= np.vstack((hand,arm))
                self.armUsed[:,0]=self.armUsed[:,0]*handlength            
                
                norm1=ExtlowerArmLengthcm+handlength
                norm2=handlength#hand image is nearly square
                div1=float(self.armUsed[:,1].max())/self.height
                div2=float(self.armUsed[:,0].max())/self.width2
                norm=div1
                self.convertPixelCm=self.height/float(norm1)
                if(div1<div2):
                    norm=div2
                    self.convertPixelCm=self.width2/float(norm2)
                self.armUsed=self.armUsed/norm  
                if(limbSide=='l'):
                    self.armUsed[:,0]=self.width2-self.armUsed[:,0]
                      
                idxWidthWrist=np.array([0, hand.shape[0]-1, hand.shape[0], self.armUsed.shape[0]-1])
                self.armUsed[idxWidthWrist,:]
                distAct=(self.armUsed[idxWidthWrist[1],0]-self.armUsed[idxWidthWrist[0],0])/self.convertPixelCm                
                if(limbSide=='l'):
                    distAct=(self.armUsed[idxWidthWrist[0],0]-self.armUsed[idxWidthWrist[1],0])/self.convertPixelCm
                    
                diff=(wristWidth-distAct)
                diffH=diff/2
                if(limbSide=='r'):
                    self.armUsed[idxWidthWrist[[0,3]],0]=self.armUsed[idxWidthWrist[[0,3]],0]-diffH*self.convertPixelCm
                    self.armUsed[idxWidthWrist[[1,2]],0]=self.armUsed[idxWidthWrist[[1,2]],0]+diffH*self.convertPixelCm
                else:
                    self.armUsed[idxWidthWrist[[0,3]],0]=self.armUsed[idxWidthWrist[[0,3]],0]+diffH*self.convertPixelCm
                    self.armUsed[idxWidthWrist[[1,2]],0]=self.armUsed[idxWidthWrist[[1,2]],0]-diffH*self.convertPixelCm
                         
                self.armUsed.round(decimals=0)
                lower=self.armUsed.copy()
                
                
                lower[:,0]=self.width-lower[:,0]
                self.armTopViewPoints=self.armUsed.tolist()
                self.armLowerViewPoints=lower.tolist()
                self.lower=lower
                self.showUpperLimb()
        
        def showUpperLimb(self):
            self.surface.fill((0,0,0))
            pygame.draw.polygon(self.surface,(150,150,150),self.armLowerViewPoints,1)
            pygame.draw.polygon(self.surface,(150,150,150),self.armTopViewPoints,1)
            self.repaint()
            
        def event(self,e):
            if self.armUsed is None: 
                return  
            if e.type == gui.MOUSEBUTTONDOWN:
                pygame.draw.line(self.surface, (255,0,0), (int(round(5*self.convertPixelCm)),self.height-int(round(0*self.convertPixelCm))), (int(round(5*self.convertPixelCm)),self.height-int(round(5*self.convertPixelCm))), 1)#check converter
#                pygame.draw.line(self.surface, (255,0,0), (int(round(14*self.convertPixelCm)),int(round(0*self.convertPixelCm))), (int(round(14*self.convertPixelCm)),int(round(17*self.convertPixelCm))), 1)#check converter
                self.repaint()
            
        def paint(self,s):
            s.blit(self.surface,(0,0))   