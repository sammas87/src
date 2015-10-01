'''
Created on 12.09.2015

@author: schneidersmatthiaserwefwe
'''
import dataObject as dO
import src.impl.control.getPortsSerial as getPortsSerial
import os

class FES():
    def __init__(self):
        #portSerialToUSB,portArduino=getPortsSerial.getPortNrAnsteuerung()
        portSerialToUSB=2
        self.__fesActivated=dO.dataObject(name='fesActivated',guiType='checkbox',label='FES',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__fesBaud=dO.dataObject(name='fesBaud',guiType='select',label='Baud:',valueType='int',actValue=38400,range='',valuesPossible=[115200, 57600, 38400, 28800, 19200,11400,9600,4800,2400,1200 ])
        self.__fesComport=dO.dataObject(name='fesComport',guiType='input',label='Comport:',valueType='int',actValue=portSerialToUSB,range=[0,20],valuesPossible='')
        self.__fesAmp=dO.dataObject(name='fesAmp',guiType='input',label='Amplitude [mA]:',valueType='int',actValue=10,range=[0,50],valuesPossible='')
        self.__fesPulse=dO.dataObject(name='fesPulse',guiType='input',label='Pulse len [ns]:',valueType='int',actValue=350,range=[50,500],valuesPossible='')
#         self.__fesFreq=dO.dataObject(name='fesFreq',guiType='input',label='Freq [hz]:',valueType='float',actValue=16.0,range=[0.5,99.5],valuesPossible=[0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0,16.5,17.0,17.5,18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,22.0,22.5,23.0,23.5,24.0,24.5,25.0,25.5,26.0,26.5,27.0,27.5,28.0,28.5,29.0,29.5,30.0,30.5,31.0,31.5,32.0,32.5,33.0,33.5,34.0,34.5,35.0,35.5,36.0,36.5,37.0,37.5,38.0,38.5,39.0,39.5,40.0,40.5,41.0,41.5,42.0,42.5,43.0,43.5,44.0,44.5,45.0,45.5,46.0,46.5,47.0,47.5,48.0,48.5,49.0,49.5,50.0,50.5,51.0,51.5,52.0,52.5,53.0,53.5,54.0,54.5,55.0,55.5,56.0,56.5,57.0,57.5,58.0,58.5,59.0,59.5,60.0,60.5,61.0,61.5,62.0,62.5,63.0,63.5,64.0,64.5,65.0,65.5,66.0,66.5,67.0,67.5,68.0,68.5,69.0,69.5,70.0,70.5,71.0,71.5,72.0,72.5,73.0,73.5,74.0,74.5,75.0,75.5,76.0,76.5,77.0,77.5,78.0,78.5,79.0,79.5,80.0,80.5,81.0,81.5,82.0,82.5,83.0,83.5,84.0,84.5,85.0,85.5,86.0,86.5,87.0,87.5,88.0,88.5,89.0,89.5,90.0,90.5,91.0,91.5,92.0,92.5,93.0,93.5,94.0,94.5,95.0,95.5,96.0,96.5,97.0,97.5,98.0,98.5,99.0,99.5])
        self.__fesFreq=dO.dataObject(name='fesFreq',guiType='input',label='Freq [hz]:',valueType='int',actValue=16,range=[1,99],valuesPossible='')
        self.__fesChannel=dO.dataObject(name='fesChan',guiType='input',label='Channel:',valueType='int',actValue=5,range=[1,8],valuesPossible='')
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__fesActivated)
        l.append(self.__fesBaud)
        l.append(self.__fesComport)
        l.append(self.__fesAmp)
        l.append(self.__fesPulse)
        l.append(self.__fesFreq)
        l.append(self.__fesChannel)
        self.__comp=l
        
    def getComponents(self):        
        return self.__comp
    
class Subject():
    def __init__(self):
        self.__subjectSubjectInformation=dO.dataObject(name='subjectSubjectInformation', guiType='none' ,label='Subjecinfo', valueType='bool',actValue=True ,range='',valuesPossible='')
        self.__subjectID=dO.dataObject(name='subjectID',guiType='input',label='ID:',valueType='string',actValue='anonym',range=[2,40],valuesPossible='')
        self.__subjectGender=dO.dataObject(name='subjectGender',guiType='select',label='Gender:',valueType='string',actValue='m',range='',valuesPossible=['m','f'])
        self.__subjectAge=dO.dataObject(name='subjectAge',guiType='input',label='Age',valueType='int',actValue=18,range=[0,130],valuesPossible='')
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__subjectSubjectInformation)
        l.append(self.__subjectID)
        l.append(self.__subjectGender)
        l.append(self.__subjectAge)
        self.__comp=l
        
    def getComponents(self):
        return self.__comp
    
class Controller():
    def __init__(self):
#         portSerialToUSB,portArduino=getPortsSerial.getPortNrAnsteuerung()
        portArduino=3
        self.__controllerController=dO.dataObject(name='controllerController',guiType='checkbox',label='Controller',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__controllerComport=dO.dataObject(name='controllerComport',guiType='input',label='Comport:',valueType='int',actValue=portArduino,range=[0,20],valuesPossible='')
        self.__controllerBaud=dO.dataObject(name='controllerBaud',guiType='select',label='Controller',valueType='int',actValue=115200,range='',valuesPossible=[115200, 57600, 38400, 28800, 19200,11400,9600,4800,2400,1200 ])
        self.__controllerChannelsUsed=dO.dataObject(name='controllerChannelsUsed',guiType='input',label='El. chan used:',valueType='listi',actValue=range(1,64+1),range=[1,64],valuesPossible='',disabled=True)
#         self.__controllerChannelN=dO.dataObject(name='controllerChannelN',guiType='input',label='N. electrodes',valueType='int',actValue=64,range=[1,64],valuesPossible='',disabled=True)
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__controllerController)
        l.append(self.__controllerComport)
        l.append(self.__controllerBaud)
        l.append(self.__controllerChannelsUsed)
#         l.append(self.__controllerChannelN)
        self.__comp=l
    
    def getComponents(self):
        return self.__comp
    
class Dataquali():
    def __init__(self):
        self.__dataqualiDataquali=dO.dataObject(name='dataqualiDataquali',guiType='none',label='Dataquali',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__dataqualiMinFramesStim=dO.dataObject(name='dataqualiMinFramesStim',guiType='input',label='Min fr stim:',valueType='int',actValue=1,range=[0,200],valuesPossible='')
        self.__dataqualiMinFramesNoStim=dO.dataObject(name='dataqualiMinFramesNoStim',guiType='input',label='Min fr no stim:',valueType='int',actValue=1,range=[0,200],valuesPossible='')
        self.__dataqualiShowEveryXImage=dO.dataObject(name='dataqualiShowEveryXImage',guiType='input',label='Subsample:',valueType='int',actValue=5,range=[-1,200],valuesPossible='')
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__dataqualiDataquali)
        l.append(self.__dataqualiMinFramesStim)
        l.append(self.__dataqualiMinFramesNoStim)
        l.append(self.__dataqualiShowEveryXImage)
        self.__comp=l
        
    def getComponents(self):
        return self.__comp
    
class Paradigma():
    def __init__(self):
        self.__paradigmaParadigma=dO.dataObject(name='paradigmaParadigma',guiType='none',label='Paradigma',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__paradigmaRepSingElec=dO.dataObject(name='paradigmaRepSingElec',guiType='input',label='Rep. sing. elec:',valueType='int',actValue=1,range=[1,200],valuesPossible='')
        self.__paradigmaRepAllElec=dO.dataObject(name='paradigmaRepAllElec',guiType='input',label='Rep. all elec:',valueType='int',actValue=1,range=[1,200],valuesPossible='')
        self.__paradigmaDurStim=dO.dataObject(name='paradigmaDurStim',guiType='input',label='Dur stim[s]:',valueType='float',actValue=1,range=[0,200],valuesPossible='')
        self.__paradigmaDurNoStim=dO.dataObject(name='paradigmaDurNoStim',guiType='input',label='Dur no stim[s]:',valueType='float',actValue=1,range=[0,200],valuesPossible='')
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__paradigmaParadigma)
        l.append(self.__paradigmaRepSingElec)
        l.append(self.__paradigmaRepAllElec)
        l.append(self.__paradigmaDurStim)
        l.append(self.__paradigmaDurNoStim)
        self.__comp=l
        
    def getComponents(self):
        return self.__comp
    
class Limb():
    def __init__(self):
        self.__limbLimb=dO.dataObject(name='limbLimb',guiType='none',label='Limb properties',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__limbLowerArmLength=dO.dataObject(name='limbLowerArmLength',guiType='input',label='L. lower arm[cm]:',valueType='float',actValue=27.0,range=[10,100],valuesPossible='')
        self.__limbWristPerimeter=dO.dataObject(name='limbWristPerimeter',guiType='input',label='P. wrist[cm]:',valueType='float',actValue=17.0,range=[5,40],valuesPossible='')
        self.__limbWristHeight=dO.dataObject(name='limbWristHeight',guiType='input',label='H. wrist[cm]:',valueType='float',actValue=4,range=[0.5,10],valuesPossible='')
        self.__limbWristWidth=dO.dataObject(name='limbWristWidth',guiType='input',label='W. wrist[cm]:',valueType='float',actValue=5.5,range=[0.5,15],valuesPossible='')
        self.__limbCubitalJointPerimeter=dO.dataObject(name='limbCubitalJointPerimeter',guiType='input',label='P. cubital jt[cm]:',valueType='float',actValue=26.0,range=[5,50],valuesPossible='')#For modelling arm is an ellipse lying at wrist, standing at cubital joint
        self.__limbCubitalJointHeight=dO.dataObject(name='limbCubitalJointHeight',guiType='input',label='H. cubital jt[cm]:',valueType='float',actValue=7.0,range=[1.5,20],valuesPossible='')
        self.__limbCubitalJointWidth=dO.dataObject(name='limbCubitalJointWidth',guiType='input',label='W. cubital jt[cm]:',valueType='float',actValue=6.0,range=[1.5,15],valuesPossible='')
        self.__limbSide=dO.dataObject(name='limbSide',guiType='select',label='Side:',valueType='string',actValue='r',range='',valuesPossible=['l', 'r'])
        self.__limbRotation=dO.dataObject(name='limbRotation',guiType='select',label='Rotation:',valueType='string',actValue='Normal',range='',valuesPossible=['Normal','Pronation','Supination'])
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__limbLimb)
        l.append(self.__limbLowerArmLength)
        l.append(self.__limbWristPerimeter)
        l.append(self.__limbWristHeight)
        l.append(self.__limbWristWidth)
        l.append(self.__limbCubitalJointPerimeter)
        l.append(self.__limbCubitalJointHeight)
        l.append(self.__limbCubitalJointWidth)
        l.append(self.__limbSide)
        l.append(self.__limbRotation)
        self.__comp=l
        
    def getComponents(self):
        return self.__comp
    
class screenGNDElectrode():
    def __init__(self):
        self.__screenGNDElectrodeOK=dO.dataObject(name='screenGNDElectrodeOK',guiType='none',label='Ground electrode properties',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__screenGNDElectrodeName=dO.dataObject(name='screenGNDElectrodeName',guiType='input',label='Name:',valueType='string',actValue='111',range=[3,100],valuesPossible='')
        self.__screenGNDElectrodeWidth=dO.dataObject(name='screenGNDElectrodeWidth',guiType='input',label='Width[cm]:',valueType='float',actValue=25.0,range=[5,40],valuesPossible='')
        self.__screenGNDElectrodeHeight=dO.dataObject(name='screenGNDElectrodeHeight',guiType='input',label='Height[cm]:',valueType='float',actValue=2,range=[0.5,10],valuesPossible='')
        self.__screenGNDElectrodeHolesDistance=dO.dataObject(name='screenGNDElectrodeHolesDistance',guiType='input',label='Distance of holes[cm]:',valueType='listf',actValue=[5.5, 4.5, 3.5, 2.5, 1.5],range=[0,15],valuesPossible='')
        self.__screenGNDElectrodeHoleDiameter=dO.dataObject(name='screenGNDElectrodeHoleDiameter',guiType='input',label='Diameter of holes[cm]:',valueType='float',actValue=0.4,range=[0.01,5],valuesPossible='')#For modelling arm is an ellipse lying at wrist, standing at cubital joint
        self.__screenGNDElectrodeNubDistance=dO.dataObject(name='screenGNDElectrodeNubDistance',guiType='input',label='Distance of Nub[cm]:',valueType='float',actValue=3.0,range=[0.1,5],valuesPossible='')
        self.__screenGNDElectrodeNubDiameter=dO.dataObject(name='screenGNDElectrodeNubDiameter',guiType='input',label='Diameter of Nub[cm]:',valueType='float',actValue=0.5,range=[0.1,5],valuesPossible='')
        self.__screenGNDElectrodeNubWElectrode=dO.dataObject(name='screenGNDElectrodeNubWElectrode',guiType='input',label='Dist. elec side nub[cm]:',valueType='listf',actValue=[5.5, 10],range=[0.01, 20],valuesPossible='',listLen=2)
        self.__screenGNDElectrodeNubHElectrode=dO.dataObject(name='screenGNDElectrodeNubHElectrode',guiType='input',label='Height elec side nub[cm]:',valueType='float',actValue=1.0,range=[0.01, 5],valuesPossible='')
        self.__screenGNDElectrodeHoleWElectrode=dO.dataObject(name='screenGNDElectrodeHoleWElectrode',guiType='input',label='Dist. elec side holes[cm]:',valueType='listf',actValue=[6.5, 12],range=[0.01, 20],valuesPossible='',listLen=2)
        self.__screenGNDElectrodeHoleHElectrode=dO.dataObject(name='screenGNDElectrodeHoleHElectrode',guiType='input',label='Height elec side holes[cm]:',valueType='float',actValue=1.0,range=[0.01, 5],valuesPossible='')
        self.__screenGNDElectrodeHoleUsed=dO.dataObject(name='screenGNDElectrodeHoleUsed',guiType='input',label='Hole used:',valueType='int',actValue=4,range=[1, 5],valuesPossible='')
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__screenGNDElectrodeOK)
        l.append(self.__screenGNDElectrodeName)
        l.append(self.__screenGNDElectrodeWidth)
        l.append(self.__screenGNDElectrodeHeight)
        l.append(self.__screenGNDElectrodeHolesDistance)
        l.append(self.__screenGNDElectrodeHoleDiameter)
        l.append(self.__screenGNDElectrodeNubDistance)
        l.append(self.__screenGNDElectrodeNubDiameter)
        l.append(self.__screenGNDElectrodeNubWElectrode)
        l.append(self.__screenGNDElectrodeNubHElectrode)
        l.append(self.__screenGNDElectrodeHoleWElectrode)
        l.append(self.__screenGNDElectrodeHoleHElectrode)
        l.append(self.__screenGNDElectrodeHoleUsed)
        self.__comp=l
        
    def getComponents(self):
        return self.__comp
    
class screenSTIMElectrode():
    def __init__(self):
        self.__screenSTIMElectrodeOK=dO.dataObject(name='screenSTIMElectrodeOK',guiType='none',label='Screen electrode properties',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__screenSTIMElectrodeName=dO.dataObject(name='screenSTIMElectrodeName',guiType='input',label='Name:',valueType='string',actValue='112',range=[3,100],valuesPossible='')
        self.__screenSTIMElectrodeWidth=dO.dataObject(name='screenSTIMElectrodeWidth',guiType='input',label='Width[cm]:',valueType='float',actValue=7.5,range=[0.1,40],valuesPossible='')
        self.__screenSTIMElectrodeHeight=dO.dataObject(name='screenSTIMElectrodeHeight',guiType='input',label='Height[cm]:',valueType='float',actValue=3.5,range=[0.5,10],valuesPossible='')
        self.__screenSTIMElectrodeWidthKnob=dO.dataObject(name='screenSTIMElectrodeWidthKnob',guiType='checkbox',label='Is Knob[cm]:',valueType='bool',actValue=True,range='',valuesPossible='')
        self.__screenSTIMElectrodeSideElectrodeConnection=dO.dataObject(name='screenSTIMElectrodeSideElectrodeConnection',guiType='select',label='Connection is on:',valueType='string',actValue='right',range='',valuesPossible=['right', 'left'])
        self.__screenSTIMElectrodeSideElectrodeDistance=dO.dataObject(name='screenSTIMElectrodeSideElectrodeDistance',guiType='input',label='Dis. from SideElect[cm]:',valueType='float',actValue=1.0,range=[0.1,5],valuesPossible='')
        self.__screenSTIMElectrodeHDistance=dO.dataObject(name='screenSTIMElectrodeHDistance',guiType='input',label='Dist. Elec to free Band[cm]:',valueType='float',actValue=0.35,range=[0.1,5],valuesPossible='')
        self.__screenSTIMElectrodeElectrodeLength=dO.dataObject(name='screenSTIMElectrodeElectrodeLength',guiType='input',label='Elec length(first to last electrode)[cm]:',valueType='float',actValue=5.5,range=[1.0, 20],valuesPossible='')
        self.__screenSTIMElectrodeElectrodeWidth=dO.dataObject(name='screenSTIMElectrodeElectrodeWidth',guiType='input',label='Elec width[cm]:',valueType='float',actValue=3.0,range=[0.01, 5],valuesPossible='')
        self.__screenSTIMElectrodePostStabil=dO.dataObject(name='screenSTIMElectrodePostStabil',guiType='input',label='Pos Stabilisator the first of the 5 stabilisators measuered from side where electrode connector is [cm]:',valueType='float',actValue=1.0,range=[0.01, 20],valuesPossible='')
        self.__screenSTIMElectrodechannelsUsed=dO.dataObject(name='screenSTIMElectrodechannelsUsed',guiType='input',label='El. chan used:',valueType='listi',actValue=range(1,15+1),range=[1,64],valuesPossible='')
        l=[]
        #Sequence here determines sequence when showed in gui, the first label indicate when everything is fine
        l.append(self.__screenSTIMElectrodeOK)
        l.append(self.__screenSTIMElectrodeName)
        l.append(self.__screenSTIMElectrodeWidth)
        l.append(self.__screenSTIMElectrodeHeight)
        l.append(self.__screenSTIMElectrodeWidthKnob)
        l.append(self.__screenSTIMElectrodeSideElectrodeConnection)
        l.append(self.__screenSTIMElectrodeSideElectrodeDistance)
        l.append(self.__screenSTIMElectrodeHDistance)
        l.append(self.__screenSTIMElectrodeElectrodeLength)
        l.append(self.__screenSTIMElectrodeElectrodeWidth)
        l.append(self.__screenSTIMElectrodePostStabil)      
        l.append(self.__screenSTIMElectrodechannelsUsed)      
        self.__comp=l
        
    def getComponents(self):
        return self.__comp
class screenTogether():
    def __init__(self):
        self.screenTogetherOK=dO.dataObject(name='screenTogetherOK',guiType='none',label='NR',valueType='bool',actValue=True,range='',valuesPossible='')
        self.screenTogetherName=dO.dataObject(name='screenTogetherName',guiType='input',label='Name:',valueType='string',actValue='test123',range=[3,100],valuesPossible='')
        self.screenTogetherX=dO.dataObject(name='screenTogetherX',guiType='input',label='X[cm]:',valueType='float',actValue=0.0,range=[0,40],valuesPossible='')
        self.screenTogetherY=dO.dataObject(name='screenTogetherY',guiType='input',label='Y[cm]:',valueType='float',actValue=0.0,range=[0,80],valuesPossible='')
        self.screenTogetherConnect=dO.dataObject(name='screenTogetherConnect',guiType='input',label='Connect[cm]:',valueType='int',actValue=-1,range=[-1,80],valuesPossible='')
        self.screenTogetherStabilisator=dO.dataObject(name='screenTogetherStabilisator',guiType='input',label='Stabilisators',valueType='listi',actValue=[0],range=[0,5],valuesPossible='')
        self.screenTogetherDist=dO.dataObject(name='screenTogetherDist',guiType='input',label='Distance[cm]:',valueType='float',actValue=0,range=[0,80],valuesPossible='')
        self.screenTogetherIsGND=False#Kein aufzulistendes Objekt
        l=[]
        l.append(self.screenTogetherOK)
        l.append(self.screenTogetherName)
        l.append(self.screenTogetherX)
        l.append(self.screenTogetherY)
        l.append(self.screenTogetherConnect)
        l.append(self.screenTogetherStabilisator)
        l.append(self.screenTogetherDist)
        self.comp=l
        
    def getComponents(self):
        return self.comp
    
class dataIO():
    def __init__(self):
        pwd=os.getcwd()
        self.pathElectrodeScreeningGround=pwd+'\\..\\rec\\electrodes\\screening\\gnd'
        self.checkPath(self.pathElectrodeScreeningGround)
        self.pathElectrodeScreening=pwd+'\\..\\rec\\electrodes\\screening\\screening'
        self.checkPath(self.pathElectrodeScreening)
        self.pathSubjects=pwd+'\\..\\rec\\subjects'
        self.checkPath(self.pathElectrodeScreening)
        
    def checkPath(self,pathToBeChecked):
        if(not os.path.isdir(pathToBeChecked)):
                os.makedirs(pathToBeChecked)

        
        
