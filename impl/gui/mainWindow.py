# -*- coding: iso-8859-15 -*-
import pygame
from src.lib.PGU.pgu import gui
# import src.lib.PGU.pgu
import Limb
import src.impl.data.dataModul as dM
import ElectrodeConfiguration as EC
import src.impl.control.recorder as recorder
import time
from src.impl.control import recorder
import src.impl.gui.showLeap as showLeap
# from multiprocessing import Process
import thread


class mainWindow:
    def __init__(self):
        self.dataIO=dM.dataIO()
        self.app=gui.Desktop()
        self.app.connect(gui.QUIT,self.app.quit,None)       
        self.layoutMain = gui.Container(width=1000,height=800)
        self.recorder=[]
        self.recordNumber=0
        w=250
        h=23
        y1=5
        x1=0
        y3=5
        x3=750
        
        x2=260
        y2=5
        
        self.subjectMod=dM.Subject()
        nElements=len(self.subjectMod.getComponents()) 
        self.subjectTab=Tabs(self.subjectMod,width=w,height=h*nElements,heightSingle=h,widthSingle=round(w/2))
        self.layoutMain.add(self.subjectTab, x1, y1)
        y1=y1+(nElements+1)*h
        
        self.limbMod=dM.Limb()
        nElements=len(self.limbMod.getComponents()) 
        self.limbTab=Tabs(self.limbMod,width=w,height=h*nElements,heightSingle=h,widthSingle=round(w/2))
        self.layoutMain.add(self.limbTab, x1, y1)
        y1=y1+(nElements+1)*h
        
        self.fesMod=dM.FES()
        nElements=len(self.fesMod.getComponents())        
        self.fesTab=Tabs(self.fesMod,width=w,height=h*nElements,heightSingle=h,widthSingle=round(w/2))
        self.layoutMain.add(self.fesTab, x3, y3)
        y3=y3+(nElements+1)*h   
        
        self.controllerMod=dM.Controller()
        nElements=len(self.controllerMod.getComponents())
        self.controllerTab=Tabs(self.controllerMod,width=w,height=h*nElements,heightSingle=h,widthSingle=round(w/2))
        self.layoutMain.add(self.controllerTab, x3, y3)
        y3=y3+(nElements+1)*h
        
        self.dataqualiMod=dM.Dataquali()
        nElements=len(self.dataqualiMod.getComponents())
        self.dataqualiTab=Tabs(self.dataqualiMod,width=w,height=h*nElements,heightSingle=h,widthSingle=round(w/2))
        self.layoutMain.add(self.dataqualiTab, x3, y3)
        y3=y3+(nElements+1)*h
        
        self.paradigmaMod=dM.Paradigma()
        nElements=len(self.paradigmaMod.getComponents())
        self.paradigmaTab=Tabs(self.paradigmaMod,width=w,height=h*nElements,heightSingle=h,widthSingle=round(w/2))
        self.layoutMain.add(self.paradigmaTab, x3, y3)
        y3=y3+(nElements+1)*h
        
        widthUL=300
        heightUL=500
        self.uL=Limb.UpperLimb(width=widthUL,height=heightUL)
        self.layoutMain.add(self.uL, x2, y2)
        y2=y2+heightUL+h
        

        ec=EC.ElectrodeConfigurator(self.uL,self.limbMod,self.controllerTab,compH=h,width=w,height=200,background=(128,128,128))
        self.layoutMain.add(ec,x1,y1)
        heighthT=200
        self.hT=showLeap.viewer(width=widthUL,height=heighthT)
        self.layoutMain.add(self.hT,x2,y2)
        y2=y2+heighthT+h
        
        self.limbTab.para[1].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.limbTab.para[2].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.limbTab.para[3].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.limbTab.para[4].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.limbTab.para[5].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.limbTab.para[6].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.limbTab.para[7].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.limbTab.para[8].connect(gui.CHANGE,self.uL.computeUpperLimb,self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value, self.limbMod.getComponents()[2].get_act_value, self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        self.uL.computeUpperLimb(self.limbMod.getComponents()[4].get_act_value,self.limbMod.getComponents()[1].get_act_value,self.limbMod.getComponents()[2].get_act_value,self.limbMod.getComponents()[8].get_act_value,self.limbTab.tabOk)
        
        self.recordB=gui.Button('Record')
        self.layoutMain.add(self.recordB,x3,y3)
        self.recordB.connect(gui.CLICK,self.doRecord)
        self.app.run(self.layoutMain)
        
        
        
    def doRecord(self):
        subOk=self.subjectTab.tabOk()
        if(not subOk):
            x=gui.Dialog(gui.Label('Failure'),gui.Label('Please enter correct subject information!'))
            x.open()
            return
        limbOk=self.limbTab.tabOk()
        if(not limbOk):
            x=gui.Dialog(gui.Label('Failure'),gui.Label('Please enter correct limb information!'))
            x.open()
            return
        fesOk=self.fesTab.tabOk()
        if(not fesOk):
            x=gui.Dialog(gui.Label('Failure'),gui.Label('Please enter correct FES information!'))
            x.open()
            return
        contrOk=self.controllerTab.tabOk()
        if(not contrOk):
            x=gui.Dialog(gui.Label('Failure'),gui.Label('Please enter correct controler information!'))
            x.open()
            return
        dataqOk=self.dataqualiTab.tabOk()
        if(not dataqOk):
            x=gui.Dialog(gui.Label('Failure'),gui.Label('Please enter correct dataquality information!'))
            x.open()
            return
        paradigmaOk=self.paradigmaTab.tabOk()
        if(not paradigmaOk):
            x=gui.Dialog(gui.Label('Failure'),gui.Label('Please enter correct paradigma information!'))
            x.open()
            return
       
        lt=time.localtime()
        year,month,day=lt[0:3]
        month2=str(month)
        if(len(month2)<2):
            month2='0'+month2
        day2=str(day)
        if(len(day2)<2):
            day2='0'+day2
        self.recordNumber=self.recordNumber+1
        path2=self.subjectMod.getComponents()[1].get_act_value()
        path=self.dataIO.pathSubjects+'\\'+path2+'\\'+str(year)+month2+day2
        self.dataIO.checkPath(path)
        x1=[]
        x1=gui.Table()
        x1.tr()
        x1.td(gui.Label('Path: '+path))
        x1.tr()
        x1.td(gui.Label('Please enter the Filename'))
        bok=gui.Button('Ok')
        x1.tr()
        self.recordInputFile=gui.Input(value='Record_'+str(self.recordNumber))
        x1.tr()
        x1.td(self.recordInputFile)
        x1.td(bok)
        self.recordInputFile.connect(gui.CHANGE,self.doRecordFileCheck, bok)
        
        y=gui.Dialog(gui.Label('Input requiered'),x1)
        y.open()
#         bok.connect(gui.CLICK, y.close)
        bok.connect(gui.CLICK, self.doRecord2,path,y)
#         self.recorder=recorder.Recorder()
    def doRecordFileCheck(self,bok):
        fileName=self.recordInputFile.value
        if(len(fileName)>0):
            bok.disabled=False
        else:
            bok.disabled=True

    def doRecord2(self,path2,y):
        y.close()
        fileName=self.recordInputFile.value
        r=True
        try:
#             self.fesMod.getComponents()[0].set_act_value(False) #TODO are not working!!!
#             self.fesMod.getComponents()[0].get_act_value(False)
            self.recorder=recorder.Recorder(self.fesMod.getComponents()[0].get_act_value(),self.fesMod.getComponents()[1].get_act_value(),self.fesMod.getComponents()[2].get_act_value(),self.fesMod.getComponents()[3].get_act_value(),self.fesMod.getComponents()[4].get_act_value(),self.fesMod.getComponents()[6].get_act_value(),self.fesMod.getComponents()[5].get_act_value(),self.controllerMod.getComponents()[0].get_act_value(),self.controllerMod.getComponents()[1].get_act_value(),self.controllerMod.getComponents()[2].get_act_value(),self.controllerMod.getComponents()[3].get_act_value(),self.paradigmaMod.getComponents()[1].get_act_value(),self.paradigmaMod.getComponents()[2].get_act_value(),self.paradigmaMod.getComponents()[3].get_act_value(),self.paradigmaMod.getComponents()[4].get_act_value(),self.dataqualiMod.getComponents()[1].get_act_value(),self.dataqualiMod.getComponents()[2].get_act_value(),self.dataqualiMod.getComponents()[3].get_act_value(),True,path2+'\\'+fileName)
        except IOError:
            r=False
        if(r):
            x=1
            x=x+1
#             a=self.recorder.run
#             b=self.hT
#             p = Process(target=a, args=(b,))
#             p.start()
#             p.join()
#             self.recorder.run(self.hT)
            thread.start_new_thread ( self.recorder.run, self.hT )
        else:
            x=gui.Table()
            x.tr()
            x.td(gui.Label('Problems with the filename, please use another one then:'+fileName+'!'))
            x2=gui.Button('OK')
            x2.connect(gui.CLICK, self.doRecord)
            x.tr()
            x.td(x2)
            y=gui.Dialog(gui.Label('Failure'),x)
            y.open()
            x2.connect(gui.CLICK, y.close)
       
        
class Tabs(gui.Container):
    def __init__(self,mod,**params):
        gui.Container.__init__(self,**params)
        elementNr=0
        self.groups=[]
        self.para=[]
        self.labels=[]
        self.components=mod.getComponents()
        heightSingle=params['heightSingle']
        widthSingle=params['widthSingle']
        allInARow=False
        if('allInARow' in params):
            allInARow=params['allInARow']
        inputSize=10
        if('inputSize' in params):
            inputSize=params['inputSize']
        showLabel=True
        if('showLabel' in params):
            showLabel=params['showLabel']
        t=-1
        for m in self.components:
            t=t+1
            label=None
            comp=None
            gr=None
            guiTyp=m.get_gui_type()
            v=m.get_act_value()
            n=m.get_name()
            label=gui.Label(value=m.get_label())
            self.labels.append(label)
            if(showLabel or t==0):
                if(allInARow):
                    self.add(label,widthSingle*(elementNr*2),0)
                else:
                    self.add(label,0,heightSingle*elementNr)            
            if(len(guiTyp)>0):
                if(guiTyp=='input'):
                    comp=gui.Input(value=v,size=inputSize)
                    comp.connect(gui.CHANGE, self.checkAndAddPara)
                elif(guiTyp=='checkbox'):
                    if(v):
                        gr=gui.Group(name=n,value=['A'])
                    else:
                        gr=gui.Group(name=n,value=[])
                    gr.connect(gui.CHANGE, self.checkAndAddPara)
                    self.groups.append(gr)
                    comp=gui.Checkbox(gr,value='A')
                if(guiTyp=='select'):
                    comp=gui.Select()
                    for s in m.get_values_possible():
                        comp.add(str(s), s)
                    comp.value=v
                    comp.connect(gui.CHANGE, self.checkAndAddPara)
            if(not comp is None):
                if(allInARow):
                    if(showLabel):
                        self.add(comp,widthSingle*(elementNr*2)+elementNr,0)
                    else:
                        self.add(comp,widthSingle*(elementNr),0)
                else:
                    if(showLabel):
                        self.add(comp,widthSingle,heightSingle*elementNr)
                    else:
                        self.add(comp,0,heightSingle*elementNr)
#             else:
#                 self.td(gui.Label(value=''))
            self.para.append(comp)
            elementNr=elementNr+1
        self.check=False
        self.checkAndAddPara()
        self.labels[0]._event(pygame.event.Event(gui.CHANGE))
                
    def checkAndAddPara(self):
        allOk=True
        disableAll=False
        groupID=0
        oldCheck=self.check;
        if(self.components[0].get_gui_type()=='checkbox'):
            if(not 'A' in self.groups[groupID].value):
                disableAll=True
            groupID=groupID+1
  
        for i in range(1, len(self.components)): #first item will not be manipulated
            actVal=None
            actOk=True
            actVal=self.para[i].value
            if(self.components[i].get_gui_type()=='input'):
                try:           
                    actOkC=self.components[i].convertFromString(actVal)
                    actOk=self.components[i].set_act_value(actOkC)
                except:
                    actOk=False
                if(actOk):
                    self.para[i].style.color=(0,255,0) 
                else:
                    allOk=False
                    self.para[i].style.color=(255,0,0)
            elif(self.components[i].get_gui_type()=='select'):
                self.components[i].set_act_value(actVal)
            elif(self.components[i].get_gui_type()=='checkbox'):
                if('A' in self.groups[groupID].value):
                    self.components[i].set_act_value(True)
                else:
                    self.components[i].set_act_value(False)
                groupID=groupID+1
            if(disableAll):
                self.para[i].disabled=True
            else:
                self.para[i].disabled=False
            if(self.components[i].get_disabled()==True):
                self.para[i].disabled=True
        self.check=allOk
        if(allOk):
            self.labels[0].style.color=(0,255,0)
        else:
            self.labels[0].style.color=(255,0,0)
        if(not oldCheck==self.check):
            self.labels[0]._event(pygame.event.Event(gui.CHANGE))
        if(disableAll):
            self.labels[0].style.color=(0,0,0)
        self.labels[0].repaint()
        
        
    def tabOk(self):
        tabOk=self.check
        if(self.components[0].get_gui_type()=='checkbox'):
            if(not 'A' in self.groups[0].value):#when tab is not used it must be ok!
                tabOk=True
        return self.check
        
            
        