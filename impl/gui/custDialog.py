'''
Created on 08.09.2015

@author: schneidersmatthias
'''
import sys, struct, os,random, time, os.path
import pygame
from src.lib.PGU.pgu import gui

class Checker():
    def checkName(self,fileName):
        return not (len(fileName)==0 or not (sum([fileNamet.islower() or fileNamet.isupper() or fileNamet.isdigit() or fileNamet=='_' or fileNamet=='.' for fileNamet in fileName]))==len(fileName) or  fileName[0].isdigit())

class OpenDialog(gui.FileDialog):
    def __init__(self,fileExt,path1,**params):
        self.fileExt=fileExt
        self.fileExtN=len(self.fileExt)
        gui.FileDialog.__init__(self,title_txt="File Browser", button_txt="Okay", cls="dialog", path=path1)                
        self.body.tr()
        self.NewDirectB=gui.Button('New Directory')
        self.NewDirectI=gui.Input(value='')
        self.NewDirectB.disabled=True  
        self.o=self.button_ok 
#         self.fnameI=self.curdir+'\\'+self.input_file.value      
        self.body.td(self.NewDirectB)                
        self.body.td(self.NewDirectI)
        self.NewDirectB.connect(gui.CLICK,self.createDir)
        self.NewDirectI.connect(gui.CHANGE, self.checkDir)
        self.checker=Checker()
        
    def _button_okay_clicked_(self, arg):
        self.path=self.curdir+'\\'+self.input_file.value
        if self.input_dir.value != self.curdir:
            if os.path.isdir(self.input_dir.value):
                self.input_file.value = ""
                self.curdir = os.path.abspath(self.input_dir.value)
                self.list.clear()
                self._list_dir_()
        else:
            self.value = os.path.join(self.curdir, self.input_file.value)
            self.send(gui.CHANGE)
            self.close()
        
        
    def createDir(self):
        if(self.NewDirectB.disabled==False):
            path=self.curdir+self.NewDirectI.value
            if(not os.path.isdir(path)):
                os.mkdir(path)
                self.checkDir()
                self._item_select_changed_(None)
            
    def checkDir(self):
        path=self.curdir+self.NewDirectI.value
        if(self.checker.checkName(self.NewDirectI.value) and not os.path.isdir(path)):
            self.NewDirectB.disabled=False
            self.NewDirectI.style.color=(0,255,0)
        else:
            self.NewDirectB.disabled=True
            self.NewDirectI.style.color=(255,0,0)
            
            
    def _list_dir_(self):
        self.input_dir.value = self.curdir
        self.input_dir.pos = len(self.curdir)
        self.input_dir.vpos = 0
        dirs = []
        files = []
        try:
            for i in os.listdir(self.curdir):
                if os.path.isdir(os.path.join(self.curdir, i)): dirs.append(i)
                else: files.append(i)
        except:
            self.input_file.value = "Opps! no access"
        dirs.sort()
        dirs = ['..'] + dirs
        
        files.sort()
        for i in dirs:
            self.list.add(i,image=self.dir_img,value=i)
        if(self.fileExtN>0):
            for i in files:
                lAkt=len(i)
                if(lAkt>self.fileExtN and i[lAkt-self.fileExtN:lAkt]==self.fileExt):
                    self.list.add(i,value=i)
        else:
            for i in files:
                self.list.add(i,value=i)
        self.list.set_vertical_scroll(0)

        


        
        
        
        
        
        
        
        
        
class SaveDialog(gui.Dialog):
    def __init__(self,fileExt,path,**params):
        title = gui.Label("Save As...")
        
        main = gui.Table()
        self.path=path
        self.fileExt=fileExt
        self.fileExtN=len(self.fileExt)
        fileSug=''
        if('fileName' in params):
            fileSug=params['fileName']
        main.tr()
        main.td(gui.Label("File: "))
        
        self.fileNameI=gui.Input(value=fileSug)
        main.td(self.fileNameI)
        self.fileNameI.connect(gui.CHANGE,self.testFile)
       
#         t.tr()
#         self.absolutePathL = gui.Label('file')
#         t.td(self.absolutePathL)
#         self.absolutePathI = gui.Input('')
#         self.absolutePathI.disabled=True
#         self.absolutePathI.style.color=self.e.color.function.disabled
#         t.td(self.absolutePathI,colspan=3)
        
        main.tr()
        self.o = gui.Button("Okay")
        self.o.connect(gui.CLICK,self.send,gui.CHANGE)
        main.td(self.o)
        
        self.c = gui.Button("Cancel")
        self.c.connect(gui.CLICK,self.close,None)
        main.td(self.c)
        self.table=main
        self.checker=Checker()
        gui.Dialog.__init__(self,title,main)
        self.testFile()
    
    
                 
    def testFile(self):
        fileIO=True
        fileName=self.fileNameI.value
#         badCharacterExist= fileName.find('/')>=0 or fileName.find('\\')>=0 or fileName.find(':')>=0   #TODO to be implemented!
        fileNameN=len(fileName)
        badCharacterExist=not self.checker.checkName(fileName)#=len(fileName)==0 or not (sum([fileNamet.islower() or fileNamet.isupper() or fileNamet.isdigit() or fileNamet=='_' or fileNamet=='.' for fileNamet in fileName]))==len(fileName) or  fileName[0].isdigit()
        if(badCharacterExist):
            fileIO=False
            print('Specialchars e.g. \\,/ or : are not allowed, use only numbers and literals(incl ''_'' and ''.''), start with a literal')
        
        fileCheckName=fileName#.copy()
        fileCheckNameN=len(fileCheckName)
        if fileCheckNameN>self.fileExtN:
            if(fileCheckName[fileCheckNameN-self.fileExtN:fileCheckNameN]==self.fileExt):
                fileCheckName=fileCheckName[0:fileCheckNameN-self.fileExtN]
        fileAbsName=self.path+'\\' +fileCheckName+self.fileExt
        if(os.path.exists(fileAbsName)):
            fileIO=False
        if(fileIO):
            self.fileNameI.style.color=(0,255,0)
            self.o.disabled=False
#             self.absolutePathI.value=fileAbsName
        else:
            self.fileNameI.style.color=(255,0,0)
            self.o.disabled=True
#             self.absolutePathI.value=''