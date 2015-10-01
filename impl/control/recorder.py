# -*- coding: iso-8859-15 -*-
'''
Created on 26.09.2015

@author: schneidersmatthias
'''
import sys, serial, os
import src.impl.data.handmodel as Handmodel
import src.impl.control.computeStimCmd as computeStimCmd
import Leap
import  random,  time
from time import sleep
import src.impl.gui.showLeap as showLeap

class Recorder:         
    def __init__(self,FESActive,FESbaud,FESport,FESAmplitude,FESPulseWidth,FESStimulationChannel,FESStimulationfrequenzy,ControllerActive,ControlePort,ControlerBaud,stimChannelUsed,repetitionsSingleElectrodeCnt,repetitionsAllEelctrodeCnt,durationStim,durationPause,minFramesStimCnt,minFramesNoStimCnt,frameSubsample,record,file):
        #return True when file can be written, else false
        self.record=record #when true it will write a file
        self.file=file      
        self.stimChannelUsed=stimChannelUsed
        self.repetitionsSingleElectrodeCnt=repetitionsSingleElectrodeCnt
        self.repetitionsAllEelctrodeCnt=repetitionsAllEelctrodeCnt
        self.durationStim=durationStim#in seconds
        self.durationPause=durationPause#in seconds
        self.minFramesStimCnt=minFramesStimCnt#repetition of trial if recorded frames is not higher while durationStim
        self.minFramesNoStimCnt=minFramesNoStimCnt #repetition of trial if recorded frames is not higher while durationPause
        self.frameSubsample=frameSubsample
        
        self.controlerActive=ControllerActive
        self.portControler=ControlePort
        self.baudControler=ControlerBaud
          
        self.FESActive=FESActive
        self.baudFES=FESbaud   
        self.portFES=FESport
        self.FESAmplitude=FESAmplitude
        self.FESPulseWidth=FESPulseWidth
        self.FESStimulationChannel=FESStimulationChannel
        self.FESStimulationfrequenzy=FESStimulationfrequenzy   
        
        #Initialisation
        self.stimChannelUsedN=len(self.stimChannelUsed)
        self.performTrial=True
        self.fileTXT=file + '.txt'        
        self.fileStimulation=file+'.stim'        
        self.fileSchaltungDerElektroden=file+'.control'
        self.fileTXThandle=-1
        self.fileStimulationhandle=-1
        self.fileContolHandle=-1
        self.frameSubsampleAct=0
       
        if(self.record):
            fileVorhanden=os.path.isfile(self.fileTXT) or os.path.isfile(self.fileStimulation) or os.path.isfile(self.fileSchaltungDerElektroden)
            if(fileVorhanden):
                raise IOError('Files already in use')
            self.fileTXThandle=open(self.fileTXT, "w")
            if (self.FESActive):
                self.fileStimulationhandle=open(self.fileStimulation, "w")
            if (self.controlerActive):
                self.fileContolHandle=open(self.fileSchaltungDerElektroden, "w")
        
        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        self.lastFrameID=0
        random.seed()       
        random.shuffle(self.stimChannelUsed)
        self.FESIsActive=-1
        self.activateControler()
        self.activateFES()
        self.timeStart=time.clock()
        self.writeTrialInfos()
        
    def activateFES(self):
        if (self.FESActive):
            self.FESSer=serial.Serial(self.portFES,self.baudFES)            
            self.deactivateFES=computeStimCmd.computeStimCmdChannel(self.FESStimulationChannel,0,0)
            self.activateFES=computeStimCmd.computeStimCmdChannel(self.FESStimulationChannel,self.FESAmplitude,self.FESPulseWidth)            
            tmpCMD=computeStimCmd.computeCmdStimulationFrequenzChannel(self.FESStimulationChannel,self.FESStimulationfrequenzy)
            self.FESSer.write(tmpCMD)            
            self.lastFESCMDTimeP=0
            self.lastFESCMDImpact=True
        else:
            self.FESSer=[]
            self.N1=[]
            self.N2=[]
        self.lastFESCMDTimeP=0
        self.lastFESCMDImpact=True
        
    def writeTrialInfos(self):
        if(self.record):
            strname=self.file+'.info'
            hinfo=open(strname, "w")
            hinfo.write(str(self.__dict__))
            hinfo.close()
            
    def activateControler(self):
        if (self.controlerActive):
            self.controlSer=serial.Serial(self.portControler,self.baudControler)
            sleep(0.8)
            self.deactivateLastControllerCMD=''
            self.activateControlerCMD=''
            self.lastControlerCMDTimeP=0
            self.lastControlCMDImpact=True
            self.controlSer.write('S5T')#arduino initialised
            self.controlSer.write('S5F')
            initialiseControl=False
            if(initialiseControl):
                sleep(2.01)
                for i in range(self.stimChannelUsedN):
                    tmpCMD='S' + str(self.stimChannelUsed[i]) + 'F'
                    print(tmpCMD);
                    self.controlSer.write(tmpCMD)                
        else:
            self.controlSer=[]
            self.N3=[]
            self.N4=[]
        self.lastControlerCMDTimeP=0
        self.lastControlCMDImpact=True

    
    
    def run(self,showLeap):
        controller=Leap.Controller() 
        sleep(0.1)
        if controller.is_connected:
            self.timeStart=time.clock()
            for SequenceRepetitionNr in range(1,self.repetitionsAllEelctrodeCnt+1):
                if(self.performTrial):
                    print('Iterationnr: %i von %i ' % (SequenceRepetitionNr, self.repetitionsAllEelctrodeCnt))
                for ElectrodeNr in range(self.stimChannelUsedN):
                    if(self.performTrial):
                        print(' ElectrodeNr: %i von %i ' % (self.stimChannelUsed[ElectrodeNr], self.stimChannelUsedN))
                        if(len(self.deactivateLastControllerCMD)>0):
                            self.controlSer.write(self.deactivateLastControllerCMD)
                            if(self.record):
                                timepoint=time.clock()-self.timeStart
                                str1=str(timepoint)+','+self.deactivateLastControllerCMD+',\n'
                                self.fileContolHandle.write(str1)
                            #sleep(0.01)
                        self.activateControlerCMD='S' +str(self.stimChannelUsed[ElectrodeNr])+'T'
                        self.deactivateLastControllerCMD='S' +str(self.stimChannelUsed[ElectrodeNr])+'F'
                        self.controlSer.write(self.activateControlerCMD)
                        #sleep(0.01)
                        if(self.record):
                            timepoint=time.clock()-self.timeStart
                            str1=str(timepoint)+','+self.activateControlerCMD+',\n'
                            self.fileContolHandle.write(str1)
                        
                        StimElecRepetitionNr=1
                        
                        while StimElecRepetitionNr < self.repetitionsSingleElectrodeCnt+1:
                            imageNoStimCnt=0
                            imageStimCnt=0
                            
                            print('  Repetition: %i of %i ' % (StimElecRepetitionNr, self.repetitionsSingleElectrodeCnt))
                            Stimulationbegin=time.clock()
                            StimulationCompleted=False
                            while(not StimulationCompleted):
                                if (self.FESActive):
                                    timeDifference=time.clock()-Stimulationbegin
                                    oldState=self.FESIsActive
                                    if(timeDifference>self.durationPause):
                                        self.FESIsActive=1
                                        if(timeDifference>(self.durationPause+self.durationStim)):
                                            StimulationCompleted=True
                                            self.FESIsActive=0
                                    else:
                                        self.FESIsActive=0
                                    if(self.FESIsActive!=oldState):
                                        self.FESActivityChanged=1
                                    else:
                                        self.FESActivityChanged=0
                                    if(self.FESActivityChanged):
                                        if(self.FESIsActive):
                                            self.FESSer.write(self.activateFES)
                                        else:
                                            self.FESSer.write(self.deactivateFES)
                                        timepoint=time.clock()-self.timeStart
                                        str1=str(timepoint)+','+str(self.FESIsActive)+',\n'
                                        self.fileStimulationhandle.write(str1)
                                frame = controller.frame()                                
                                pictRecorded=self.doFrameComputation(frame,showLeap)
                                if(pictRecorded):
                                    if(self.FESIsActive):
                                        imageStimCnt=imageStimCnt+1
                                    else:
                                        imageNoStimCnt=imageNoStimCnt+1                                
                            if(imageStimCnt>self.minFramesStimCnt and imageNoStimCnt>self.minFramesNoStimCnt):
                                StimElecRepetitionNr=StimElecRepetitionNr+1;
                            else:
                                print('additional Repetition, bad image quality!'+str(imageStimCnt)+'/'+str(self.minFramesStimCnt)+', '+str(imageNoStimCnt)+'/'+str(self.minFramesNoStimCnt))            
        else:
            print('Please connect the controller')   
        if (self.FESActive):
            self.FESSer.write(self.deactivateFES)
        if (self.controlerActive):
            self.controlSer.write(self.deactivateLastControllerCMD)
        if(self.record):
            self.fileTXThandle.close()
            if (self.FESActive):
                self.fileStimulationhandle.close()
            if (self.controlerActive):
                timepoint=time.clock()-self.timeStart
                str1=str(timepoint)+','+self.deactivateLastControllerCMD+',\n'
                self.fileContolHandle.write(str1)
                self.fileContolHandle.close()
            
        
    def beende2(self):
        self.performTrial=False
        
    def doFrameComputation(self,frame,showLeap):        
        pictRecorded=False
        if frame.is_valid and self.lastFrameID !=frame.id:                    
            self.lastFrameID =frame.id
            hands = frame.hands
            if not hands.is_empty and hands.leftmost == hands.rightmost: #Genau eine Hand ist sichtbar
                hand=hands.rightmost
                fingers = hand.fingers
                if hand.is_valid and hand.confidence>0.2:
                    arm=hand.arm
                    if arm.is_valid:
                        #sleep(0.05)
                        #get coordinates of Hand
                        handm=Handmodel.Handmodel()
                        #x=Handmodel.Node(hand.wrist_position,'Handgelenk',hand.is_valid)
                        #handm.addNode(Handmodel.Node(hand.wrist_position.x,hand.wrist_position.y,hand.wrist_position.z,'Handgelenk',hand.is_valid))
                        handm=self.addFingers(handm,fingers)
                        handm.addNode(Handmodel.Node(self.gW(hand.wrist_position),'wrist',hand.is_valid))#Bei diesem und den nachfolgenden zweien sind die Wert schon zuvor auf True überprüft worden...
                        handm.addNode(Handmodel.Node(self.gW(arm.elbow_position),'elbow',arm.is_valid))
                        #handm.addNode(Handmodel.Node(self.gW(hand.palm_normal),'palm',hand.is_valid))# sollte eigentlich palm_position sein...
                        #handm.infoNodes()
                        if(self.record):
                            self.fileTXThandle.write(handm.infoNodes(0,time.clock()))
                        self.frameSubsampleAct=self.frameSubsampleAct+1
                        if(self.frameSubsampleAct-self.frameSubsample>=0 and self.frameSubsample>-1):
                            self.frameSubsampleAct=0
                            showLeap.FrameComputation(handm)
                       
                        pictRecorded=True
                    else:
                        print('Armmodel not correct')
                else:
                    print('Handmodel not correct')

        return pictRecorded
    
    def addFingers(self,handm,fingers):
        handm=self.addFinger(handm,fingers,Leap.Finger.TYPE_THUMB,1)
        handm=self.addFinger(handm,fingers,Leap.Finger.TYPE_INDEX)
        handm=self.addFinger(handm,fingers,Leap.Finger.TYPE_MIDDLE)
        handm=self.addFinger(handm,fingers,Leap.Finger.TYPE_RING)
        handm=self.addFinger(handm,fingers,Leap.Finger.TYPE_PINKY)
        return handm
    
    def addFinger(self,handm,fingers,fingerTyp,ignoreProxi=0):
        if not ignoreProxi:
            f=fingers[fingerTyp].bone(Leap.Bone.TYPE_METACARPAL)
            handm.addNode(Handmodel.Node(self.gW(f.prev_joint),[self.finger_names[fingerTyp] + str(Leap.Bone.TYPE_METACARPAL)],f.is_valid))
        f=fingers[fingerTyp].bone(Leap.Bone.TYPE_PROXIMAL)
        handm.addNode(Handmodel.Node(self.gW(f.prev_joint),[self.finger_names[fingerTyp] + str(Leap.Bone.TYPE_PROXIMAL)],f.is_valid))
        f=fingers[fingerTyp].bone(Leap.Bone.TYPE_INTERMEDIATE)
        handm.addNode(Handmodel.Node(self.gW(f.prev_joint),[self.finger_names[fingerTyp] + str(Leap.Bone.TYPE_INTERMEDIATE)],f.is_valid))
        f=fingers[fingerTyp].bone(Leap.Bone.TYPE_DISTAL)
        handm.addNode(Handmodel.Node(self.gW(f.prev_joint),[self.finger_names[fingerTyp] + str(Leap.Bone.TYPE_DISTAL)],f.is_valid))
        handm.addNode(Handmodel.Node(self.gW(f.next_joint),[self.finger_names[fingerTyp] + str(Leap.Bone.TYPE_DISTAL+1)],f.is_valid)) 
        return handm

    def gW(self,leapVec):
        a=(leapVec.x,leapVec.y,leapVec.z)
        return a


