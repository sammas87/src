# -*- coding: iso-8859-15 -*-
'''
Created on 13.09.2015

@author: schneidersmatthias
'''
import pygame
from src.lib.PGU.pgu import gui
import mainWindow as mW
import src.impl.data.dataModul as dM
import src.impl.gui.custDialog as cD
import numpy as np

class ElectrodeConfigurator(gui.Container):
    def __init__(self,uL,limbMod,controllerTab,**params):
        gui.Container.__init__(self,**params)
        self.chooser=gui.Select()
        self.chooser.add('Screening','screening')
        self.chooser.add('gloveBjoern','gloveBjoern')
        self.chooser.add('test','test')
        self.chooser.value='screening'
        self.chooser.value='test'
        self.add(self.chooser, params['width']/2, 0)
        self.chooser.connect(gui.CHANGE, self.layoutUseElectrode)
        self.compH=params['compH']
        self.controllerTab=controllerTab
        params['height']=params['height']-params['compH']
        params['background']=(0,128,0)
        self.screeningWidget=ScreeningWidget(uL,limbMod, self.controllerTab.para[3],self.controllerTab.components[3],**params)
        self.layoutUseElectrode()
        
    def layoutUseElectrode(self):
        try:          
            if(len(self.widgets)>1):
                self.remove(self.widgets[1])
            if(self.chooser.value=='test'):
                self.controllerTab.para[3].disabled=False
                self.controllerTab.components[3].set_disabled(False)
                self.controllerTab.para[3]._event(pygame.event.Event(gui.CHANGE))
            elif(self.chooser.value=='gloveBjoern'):
                a=1#To be implemented!
                self.controllerTab.para[3].disabled=True
                self.controllerTab.components[3].set_disabled(True)
                self.controllerTab.para[3]._event(pygame.event.Event(gui.CHANGE))
            elif(self.chooser.value=='screening'):
                self.controllerTab.para[3].value='[]'
                self.controllerTab.para[3].disabled=True
                self.controllerTab.components[3].set_disabled(True)
                self.controllerTab.para[3]._event(pygame.event.Event(gui.CHANGE))
                self.add(self.screeningWidget, 0, self.compH)
                
        except:
            a=1
            
class ScreeningElectrodeDialog(gui.Dialog):
    def __init__(self,parent,**params):
        self.contentModWidthSingle=params['width']/2
        self.contentModHeightSingle=params['compH']
        self.title=params['title']
        self.electrodeType=params['electrodeType']
        self.io=dM.dataIO()
        self.parent=parent
        self.newButton()
        

        
    def addDialogs(self):
        if(self.electrodeType=='GND'):
            self.contentMod=dM.screenGNDElectrode()
            self.saveDialog=cD.SaveDialog('.screen.gnd.elec',self.io.pathElectrodeScreeningGround)
            self.saveB.connect(gui.CLICK,self.saveDialog.open);
            self.saveDialog.o.connect(gui.CLICK,self.save)
            self.loadDialog=cD.OpenDialog('.screen.gnd.elec',self.io.pathElectrodeScreeningGround)
            self.loadB.connect(gui.CLICK,self.loadDialog.open)
            self.loadDialog.o.connect(gui.CLICK,self.load)
        elif(self.electrodeType=='Stim'):
            self.contentMod=dM.screenSTIMElectrode()
            self.saveDialog=cD.SaveDialog('.screen.stim.elec',self.io.pathElectrodeScreening)
            self.saveB.connect(gui.CLICK,self.saveDialog.open);
            self.saveDialog.o.connect(gui.CLICK,self.save)
            self.loadDialog=cD.OpenDialog('.screen.stim.elec',self.io.pathElectrodeScreening)
            self.loadB.connect(gui.CLICK,self.loadDialog.open)
            self.loadDialog.o.connect(gui.CLICK,self.load)
        self.nElements=len(self.contentMod.getComponents())
        self.contentModHeight=self.contentModHeightSingle*self.nElements
        self.content=mW.Tabs(self.contentMod,height=self.contentModHeight ,widthSingle=self.contentModWidthSingle,heightSingle=self.contentModHeightSingle)
        
    def add(self):
        b=1
        b=b+1
        actNameExist=False
        electrodeDetail=self.contentMod.getComponents()
        actName=electrodeDetail[1].get_act_value()
        for electrode in self.parent.ListElectrodes:
            if(electrode.screenTogetherName.get_act_value()==actName):
                x=gui.Dialog(gui.Label('Failure'),gui.Label('Please choose another electrodename!'))
                x.open()
                actNameExist=True
                return
        electrodeUseful=False
        if(self.electrodeType=='GND'):
            if(self.parent.NGND<1):
                electrodeUseful=True
        else:
            if(self.parent.NStim<4):
                electrodeUseful=True
                #Test ob Kanaele schon vorhanden
                if(len(self.parent.channelGui.value)>2):
                    intersection=set(self.parent.channelComp.get_act_value()).intersection(electrodeDetail[11].get_act_value())
                    if(not len(intersection)==0):
                        x=gui.Dialog(gui.Label('Failure'),gui.Label('Channel(s):' + str(intersection)+' already used !'))
                        x.open()
                        return
                
                
        if(not electrodeUseful):
            x=gui.Dialog(gui.Label('Failure'),gui.Label('Please use another Electrodetype(max 1 GND and 4 Stimuchannels)!'))
            x.open()
            return
            
        
        
        if(not actNameExist and electrodeUseful):

            actObj=dM.screenTogether()
            actObjComp=actObj.getComponents()
            actObj.screenTogetherName.set_act_value(actName)
            actObj.screenTogetherOK.set_label(str(self.parent.ListElectrodesNumbers))
            self.parent.ListElectrodesNumbers=self.parent.ListElectrodesNumbers+1
            if(self.electrodeType=='GND'):
                actObj.screenTogetherIsGND=True
                self.parent.NGND=self.parent.NGND+1
                self.electrodePlot=ScreeningPlotGND(self.parent.uL ,self.parent.limbMod,actObj,self.contentMod)
            else:
                actObj.screenTogetherIsGND=False
                self.parent.NStim=self.parent.NStim+1
                #             hier müssen die Kanäle ind die gui einsortiert werden
                tmp=str(electrodeDetail[11].get_act_value())
                if(len(self.parent.channelGui.value)>2):
                    self.parent.channelGui.value=self.parent.channelGui.value[0:len(self.parent.channelGui.value)-1]+', '+tmp[1:len(tmp)]
                else:
                    self.parent.channelGui.value=tmp
                self.parent.channelGui._event(pygame.event.Event(gui.CHANGE))
            actPara=mW.Tabs(actObj,allInARow=True,inputSize=2,showLabel=False,widthSingle=self.parent.smallWidth,heightSingle=self.contentModHeightSingle)
            self.parent.ListElectrodes.append(actObj)
            self.parent.ListElectrodesParas.append(actPara)
            self.parent.ListElectrodesDetails.append(self.contentMod)
            y=self.contentModHeightSingle*(len(self.parent.ListElectrodes)+1)
            self.parent.add(actPara,0,y)
            n=len(actObjComp)
            o=-5
            buttonU=gui.Button('U',width=self.parent.smallWidth+o,height=self.parent.smallWidth)
            x=(n+0)*self.parent.smallWidth
            self.parent.add(buttonU,x,y)
            
            self.parent.ListButtons.append(buttonU)
            buttonD=gui.Button('D',width=self.parent.smallWidth+o,height=self.parent.smallWidth)
            x=(n+1)*self.parent.smallWidth
            self.parent.add(buttonD,x,y)
            self.parent.ListButtons.append(buttonD)
            buttonX=gui.Button('X',width=self.parent.smallWidth+o,height=self.parent.smallWidth,color=(255,0,0))
            
            x=(n+2)*self.parent.smallWidth
            self.parent.add(buttonX,x,y)            
            self.parent.ListButtons.append(buttonX)
            
            buttonD.connect(gui.CLICK, self.moveElectrode,actName,'D')
            buttonU.connect(gui.CLICK, self.moveElectrode,actName,'U')
            buttonX.connect(gui.CLICK, self.deleteElectrode, actName)
            
            
            self.newButton()
            self.close()
        
            
    def callTest(self):
        if(hasattr(self, 'electrodePlot')):
            self.electrodePlot.test()

    def moveElectrode(self,electrodeName,direction):
#         return# To be implemented! Ist noch fehlerhaft!
        i=0
        wasConnectedWith=-1
        for electrode in self.parent.ListElectrodes:
            if(electrode.screenTogetherName.get_act_value()==electrodeName):
                if(self.parent.ListElectrodes[i].screenTogetherConnect.get_act_value()>0):
                    wasConnectedWith=self.parent.ListElectrodes[i].screenTogetherConnect.get_act_value()
                    break
            i=i+1 
        i=0
        y=0
        height=0
        handBeginY=0#muss aus der Figure geholt werden!
        handEndY=300#muss aus der Figure geholt werden!
        for electrode in self.parent.ListElectrodes:
            if(not electrode.screenTogetherName.get_act_value()==electrodeName and not electrode.screenTogetherName.get_act_value()==wasConnectedWith and not electrode.screenTogetherIsGND):
                y=float(self.parent.ListElectrodesParas[i].para[3].value)
                height=self.parent.ListElectrodesDetails[i].getComponents()[3].get_act_value()
                break
            i=i+1
        i=0
        for electrode in self.parent.ListElectrodes:
            if(electrode.screenTogetherName.get_act_value()==electrodeName or electrode.screenTogetherName.get_act_value()==wasConnectedWith):
                y1=float(self.parent.ListElectrodesParas[i].para[3].value)
                height1=self.parent.ListElectrodesDetails[i].getComponents()[3].get_act_value()
                if(direction=='U'):
                    if((y-height1)>=handBeginY):
                        self.parent.ListElectrodesParas[i].para[3].value=(y-height1)
                        self.parent.ListElectrodesParas[i].para[3]._event(pygame.event.Event(gui.CHANGE))
                        self.parent.ListElectrodesParas[i].para[5].value='[0]'
                        self.parent.ListElectrodesParas[i].para[5]._event(pygame.event.Event(gui.CHANGE))                        
                elif(direction=='D'):
                    if((y+height)<=handEndY):
                        self.parent.ListElectrodesParas[i].para[3].value=(y+height)
                        self.parent.ListElectrodesParas[i].para[3]._event(pygame.event.Event(gui.CHANGE))
                        self.parent.ListElectrodesParas[i].para[5].value='[0]'
                        self.parent.ListElectrodesParas[i].para[5]._event(pygame.event.Event(gui.CHANGE))
            i=i+1
             
    def deleteElectrode(self,electrodeName):
        i=0
        idxYUp=0
        wasConnectedWith=-1
        for electrode in self.parent.ListElectrodes:
            if(electrode.screenTogetherName.get_act_value()==electrodeName):
                iv=range((i*3),(i*3)+2+1)
                j=2
                while j>=0:
                    self.parent.remove(self.parent.ListButtons[iv[j]])
                    del(self.parent.ListButtons[iv[j]])
                    j=j-1
                if(len(self.parent.channelGui.value)>2):
                    toBeDeletet=self.parent.ListElectrodesDetails[i].getComponents()[11].get_act_value()
                    res=set(self.parent.channelComp.get_act_value()).difference(toBeDeletet)
                    if(len(res)>0):
                        self.parent.channelComp.set_act_value(list(res))
                        self.parent.channelGui.value=str(list(res))
                    else:
                        self.parent.channelGui.value='[]'#TODO es werden nicht die angezeigten Texte geupdatet :(
                    self.parent.channelGui._event(pygame.event.Event(gui.CHANGE))
               
                    
                                                                 
                self.parent.remove(self.parent.ListElectrodesParas[i])
#                 del self.parent.ListButtons[iv]
                if(electrode.screenTogetherIsGND):
                    self.parent.NGND=self.parent.NGND-1
                else:
                    self.parent.NStim=self.parent.NStim-1
                
                if(self.parent.ListElectrodes[i].screenTogetherConnect.get_act_value()>0):
                    wasConnectedWith=self.parent.ListElectrodes[i].screenTogetherConnect.get_act_value()
                del self.parent.ListElectrodes[i]
                del self.parent.ListElectrodesParas[i]
                del self.parent.ListElectrodesDetails[i]
#                 self.newButton()
#                 self.close()
                idxYUp=i
            i=i+1
        if(wasConnectedWith>-1):
            for electrode in self.parent.ListElectrodesParas:
                if(int(electrode.components[0].get_label())==wasConnectedWith):
                    electrode.para[4].value='-1'
                    electrode.para[4]._event(pygame.event.Event(gui.CHANGE))
                    break
                
        for i in range(idxYUp,len(self.parent.ListElectrodes))[::-1]:
            iv=range((i*3),(i*3)+2+1)
            j=2
            while j>=0:
                self.parent.ListButtons[j].style.y=self.parent.ListButtons[j].style.y-self.parent.smallWidth
                j=j-1
            self.parent.ListElectrodesParas[i].style.y=self.parent.ListElectrodesParas[i].style.y-self.parent.smallWidth
                    
            
    def load(self):
#         self.loadDialog.
        file=self.loadDialog.input_dir.value+'\\'+self.loadDialog.input_file.value
        f=open(file,'r')
        c=self.contentMod.getComponents()
        p=self.content.para
        g=self.content.groups
        r= range(1, len(c))#0element is just the description of the tab
        groupID=0
        if(c[0].get_gui_type()=='checkbox'):
            if(not 'A' in g[groupID].value):
                disableAll=True
            groupID=groupID+1
        i=0
        for line in f:
            if(i>0):
                nextIdx=line.find(',')
                if(nextIdx>=0):                
                    keyName=line[0:nextIdx]
                    keyValue=line[nextIdx+1:len(line)-1].strip()
                    if(c[i].get_name()==keyName):
                        if(c[i].get_gui_type()=='input'):       
                            p[i].value=keyValue
                        elif(c[i].get_gui_type()=='select'):
                            p[i].value=keyValue
                        elif(c[i].get_gui_type()=='checkbox'):
                            if(keyValue=='True'):
                               g[groupID].value=['A']
                            else:
                                g[groupID].value=[]
                            groupID=groupID+1  
                    else:
                        print('Unknown: ' +keyName )
            i=i+1
        self.content.checkAndAddPara()                
        self.loadDialog.close()
        
    def save(self):
        if(len(self.saveDialog.path)>0):
            file=self.saveDialog.path+'\\'+self.saveDialog.fileNameI.value+self.saveDialog.fileExt
            f=open(file,'w')
            for comp in  self.contentMod.getComponents():
                f.write(comp.get_name()+', '+str(comp.get_act_value())+'\n' )            
            f.close()  
        self.saveDialog.close()
        
    def newButton(self):
        t=0
        if(hasattr(self, 'layout')):
            #save old values
            self.layout.clear()
            t=1#workaround Dialog in the center
        self.clear()
        self.layout = gui.Table()
        self.newB=gui.Button('New')
        self.loadB=gui.Button('Load')
        self.saveB=gui.Button('Save')
        self.addB=gui.Button('Add')        
        title=gui.Label(self.title)
        self.addDialogs()        
        self.addB.connect(gui.CLICK,self.add)  
        self.layout.tr()
        self.layout.td(self.newB)
        self.layout.td(self.loadB)
        self.layout.tr()
        self.layout.td(self.content,colspan=2)
        self.layout.tr()
        self.layout.td(self.saveB)
        self.layout.td(self.addB)       
        self.newB.connect(gui.CLICK, self.newButton)
        self.content.labels[0].connect(gui.CHANGE,self.deActivateSaveAddButton)
        self.deActivateSaveAddButton()       
        gui.Dialog.__init__(self,title,self.layout)
#         self.resize()#hier wird es nicht von table sondern von theme aufgerufen k.P. warum!
        if(t):
            self.close()
            self.open()


        
        
    def deActivateSaveAddButton(self):
        if self.content.check:
            self.addB.disabled=False
            self.saveB.disabled=False
        else:
            self.addB.disabled=True
            self.saveB.disabled=True
        
class ScreeningPlotGND():
    def __init__(self,uL,limbMod,together,details):
        self.uL=uL
        self.limbMod=limbMod
        self.limbComp=limbMod.getComponents()
        self.together=together
        self.details=details
        self.detailsComp=details.getComponents()
        
    def test(self):
        limbSide=self.limbComp[8].get_act_value()
        limbPeri=self.limbComp[2].get_act_value()
        limbPeri2=limbPeri/2
        elecW=self.detailsComp[2].get_act_value()
        elecH=self.detailsComp[3].get_act_value()
        c=self.uL.convertPixelCm
        wristw=self.limbComp[4].get_act_value()
        
        HoleAt=elecW-limbPeri
        holesAvailable=self.detailsComp[4].get_act_value()
        holeUsed=self.detailsComp[12].get_act_value()-1
        periVorhanden=elecW-holesAvailable[holeUsed]
        c=self.uL.convertPixelCm
        if(limbSide=='r'):
            idxHand=self.uL.PointsHand.shape[0]        
            x0_t=self.uL.armUsed[0,0]
            y0_t=self.uL.armUsed[0,1]
            x0_l=self.uL.lower[idxHand,0]
            y0_l=self.uL.lower[idxHand,1]
        else:
            idxHand=self.uL.PointsHand.shape[0]
            x0_t=self.uL.armUsed[idxHand,0]
            y0_t=self.uL.armUsed[idxHand,1]
            x0_l=self.uL.lower[0,0]
            y0_l=self.uL.lower[0,1]
            
#         print(str(x0_t/c)+', '+str(y0_t/c)+' beginn')
#         print(str(x0_l/c)+', '+str(y0_l/c)+' beginn')
        lElectrode2=periVorhanden/2
        w=wristw
        h=elecH
#    TODO:     weiter mit: E:\workspace\Screening2\misc\3dVorversuche ->Idee die 2d kann ich hier aus dem Punkteteppich berechnenlassen!
        color=(220,220,220)        
        cordsT=(int(round(x0_t)),int(round(y0_t)),int(round(w*c)),int(round(h*c)))
        cordsL=(int(round(x0_l)),int(round(y0_l)),int(round(w*c)),int(round(h*c)))
        pygame.draw.rect(self.uL.surface,color,cordsT,0)
        pygame.draw.rect(self.uL.surface,color,cordsL,0)
        self.uL.repaint()
            
            
class ScreeningWidget(gui.Container):
    def __init__(self,uL,limbMod,channelGui,channelComp,**params):
            gui.Container.__init__(self,**params)
            self.width=params['width']
            self.height=params['height']
            self.channelGui=channelGui
            self.channelComp=channelComp
            self.uL=uL
            self.limbMod=limbMod
            compH=params['compH']
            self.buttonGround=gui.Button('Groundelec',width=round(self.width/2)-20,height=compH)
            self.add(self.buttonGround,0,0)            
            self.GNDDialog=ScreeningElectrodeDialog(self,title='Ground electrode:',electrodeType='GND',**params)
            self.buttonGround.connect(gui.CLICK,self.GNDDialog.open)
            self.buttonStim=gui.Button('Stimelec',width=round(self.width/2)-20,height=compH)
            self.add(self.buttonStim,round(self.width/2),0)
            self.StimDialog=ScreeningElectrodeDialog(self,title='Stimulation electrode:',electrodeType='Stim',**params)
            self.buttonStim.connect(gui.CLICK, self.StimDialog.open)
            self.ListElectrodesDetails=[]
            self.ListElectrodes=[]
            self.ListElectrodesParas=[]
            self.ListButtons=[]
            self.ListElectrodesNumbers=0
            self.smallWidth=25
            self.add(gui.Label('#'),0*self.smallWidth,compH)
            self.add(gui.Label('\'\''),1*self.smallWidth,compH)
            self.add(gui.Label('X'),2*self.smallWidth,compH)
            self.add(gui.Label('Y'),3*self.smallWidth,compH)
            self.add(gui.Label('C'),4*self.smallWidth,compH)
            self.add(gui.Label('S'),5*self.smallWidth,compH)
            self.add(gui.Label('D'),6*self.smallWidth,compH)
            self.NGND=0
            self.NStim=0
            tesButton=gui.Button('Test')
            tesButton.connect(gui.CLICK, self.GNDDialog.callTest)
            self.add(tesButton,0,200)
#             gndDialog=GNDDialog(e,params['param'])
#             self.buttons.ground.connect(gui.CLICK,gndDialog.open,None)