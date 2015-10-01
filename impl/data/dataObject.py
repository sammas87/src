# -*- coding: iso-8859-15 -*-
'''
Created on 12.09.2015

@author: schneidersmatthias
'''

import sys, os

class myStruct():
	def __init__(self):
		xsadsadasd=0

class dataObject:
	### General properties of every param which is shown on the gui
	def __init__(self,**params):
		self.__listLen=''
		if('listLen' in params):
			if(params['listLen']>0):
				self.__listLen=params['listLen']
			else:
				raise ValueError( 'Wrong Value for listLen!')
		self.__disabled=False
		if('disabled' in params):
			self.__disabled=params['disabled']
		self.__guiType=''
		if('guiType' in params):
			self.set_gui_type(params['guiType'])
		self.__label=''
		if('label' in params):
			self.__label=params['label']
		self.__valueType=''
		if('valueType' in params):
			self.set_value_type(params['valueType'])
		
		self.__range=''	#Only to be used when datatyp is value int,float or string, when used for the last one it is used for the property length
		if('range' in params):
			self.set_range(params['range'])
		self.__valuesPossible=''	#for Item Select
		if('valuesPossible' in params):
			self.__valuesPossible=params['valuesPossible']
		self.__name=''#under this name will the parameter be stored
		if('name' in params):
			self.__name=params['name']
		
		self.__actValue=''
		if('actValue' in params):
			self.set_act_value(params['actValue'])
		
		

	def get_list_len(self):
	    return self.__listLen


	def get_disabled(self):
	    return self.__disabled


	def set_list_len(self, value):
	    self.__listLen = value


	def set_disabled(self, value):
	    self.__disabled = value


	def del_list_len(self):
	    del self.__listLen


	def del_disabled(self):
	    del self.__disabled

			



		
		#dataObject(name='',guiType='',label='',valueType='',actValue='',range='',valuesPossible='')
	def convertToString(self,value):
		return str(value)
	
	def convertFromString(self,value):
		erg=None
		if(self.__valueType=='int'):
			erg=int(value)
		elif(self.__valueType=='float'):
			erg=float(value)
		elif(self.__valueType=='bool'):
			erg=bool(value)
		elif(self.__valueType=='string'):
			erg=str(value)
		elif(len(self.__valueType)>4 and self.__valueType[0:4]=='list'):
			isOk,erg=self.checkListType(value,False)
			if(erg is None or not isOk):
				raise ValueError( 'Convertion is not possible!')
		else:
			raise ValueError( 'Convertion is not possible!')
		return erg
	
	def checkListType(self,value,checkNotConvert):
		oldValueType=self.__valueType
		oldActValue=self.__actValue[:]
		isOk=True
		try:
			if(self.__valueType[4]=='i'):
				self.__valueType='int'
			elif(self.__valueType[4]=='f'):
				self.__valueType='float'
			elif(self.__valueType[4]=='b'):
				self.__valueType='bool'
			elif(self.__valueType[4]=='s'):
				self.__valueType='string'
			if(checkNotConvert):
				isOk=self.__check_List(value)
				if(isOk):
					erg=value
				else:
					erg=None
			else:
				isOk,erg=self.__convert_List(value)
		except:
			isOk=False
			erg=None
		self.__valueType=oldValueType
		self.__actValue=oldActValue[:]
		return isOk,erg	
		
	def __check_List(self,liste):
		erg=True
		for j in liste:
			if not self.set_act_value(j):
				erg=False
		return erg
	
	def __convert_List(self,listeStr):  
		listeStr=listeStr.strip()
		var=[]     
		try:
			varC=True
			if(listeStr[0]=='[' and listeStr[len(listeStr)-1]==']'):
				contSearch=True
				listeStr=listeStr[1:len(listeStr)-1]
				nextIdx=listeStr.find(', ')
				var=[]
				while(nextIdx>0):
					endIdx=(nextIdx-1)
					tmp=0
					if(endIdx>0):
						tmp=self.convertFromString(listeStr[0:endIdx+1])
					else:
						tmp=self.convertFromString(listeStr[0])
					if self.set_act_value(tmp):
						var.append(tmp)
					else:
						varC=False
					listeStr= listeStr[endIdx+3:len(listeStr)]
					nextIdx= listeStr.find(', ')
			if(len(listeStr)>0):
				tmp=self.convertFromString(listeStr)
				if self.set_act_value(tmp):
					var.append(tmp)
				else:
					varC=False
			if(len(var)<=0):
				varC=False
		except:
			varC=False
		return varC,var
	
	def checkData(self):
		actOk=True
		if(len(self.__valueType)>4 and self.__valueType[0:4]=='list'):
			actOk,erg=self.checkListType(self.__actValue,True)
			if(not self.__listLen==''):
				if(not len(erg)==self.__listLen):
					actOk=False
		else:
			if(len(self.__valuesPossible)==0):
				if(self.__valueType=='float' or self.__valueType=='int'):
					if len(self.__range)>0:
						if(not (self.__actValue>=self.__range[0] and self.__actValue<=self.__range[1])):
							actOk=False
				elif(self.__valueType=='string'):
					b=len(self.__actValue)
					if len(self.__range)>0:
						if(not (b>=self.__range[0] and b<=self.__range[1])):
							actOk=False
			else:
				if(not(self.__actValue in self.__valuesPossible)):
					actOk=False
		return actOk
		

	def get_gui_type(self):
	    return self.__guiType


	def get_label(self):
	    return self.__label


	def get_value_type(self):
	    return self.__valueType


	def get_act_value(self):
	    return self.__actValue


	def get_range(self):
	    return self.__range


	def get_values_possible(self):
	    return self.__valuesPossible


	def set_gui_type(self, value):
		value.lower()
		value.strip()
		if(value=='input' or value=='checkbox' or value=='select' or value=='none'):
			self.__guiType = value
		else:
			raise ValueError( 'GUI type: '+value+' is not yet implemented!')


	def set_label(self, value):
	    self.__label = value


	def set_value_type(self, value):
		value.lower()
		value.strip()
		if(value=='int' or value=='float' or value=='bool' or value=='string' or (len(value)>4 and value[0:4]=='list')):
			self.__valueType = value
		else:
			raise ValueError( 'Value type: '+value+' is not yet implemented!')


	def set_act_value(self, value):
		oldValue=self.__actValue
		self.__actValue = value
		valueOK=True
		try:
			valueOK=self.checkData()
		except:
			valueOK=False
		if(not valueOK):
			self.__actValue=oldValue
		return valueOK


	def set_range(self, value):
		if(len(value)==0):
			self.__range = value
		elif(len(value)==2):
			if(value[0]<value[1]):
				self.__range = value
			else:
				raise ValueError( 'Range: '+ str(range[0]) +' must be smaller than '+ str(range[1]))
		else:
			raise ValueError( 'Range: '+ str(range) +' must be \'\' or [a,b], where a is < b')
	    	


	def set_values_possible(self, value):
	    self.__valuesPossible = value


	def del_gui_type(self):
	    del self.__guiType


	def del_label(self):
	    del self.__label


	def del_value_type(self):
	    del self.__valueType


	def del_act_value(self):
	    del self.__actValue


	def del_range(self):
	    del self.__range


	def del_values_possible(self):
	    del self.__valuesPossible
	    
	def get_name(self):
	    return self.__name


	def set_name(self, value):
	    self.__name = value


	def del_name(self):
	    del self.__name


	guiType = property(get_gui_type, set_gui_type, del_gui_type, "Type is input, checkbox, select, or none, then is there just a label... TODO add radiobutton etc....")
	label = property(get_label, set_label, del_label, "Description of the parameter on GUI")
	valueType = property(get_value_type, set_value_type, del_value_type, "Type of the parameter int, float, boolean, string,list(beta)")
	actValue = property(get_act_value, set_act_value, del_act_value, "The actual value, at loading time it's the default value shown in GUI ")
	range = property(get_range, set_range, del_range, "For checking if the number ic correct, 2 elements, min and max")
	valuesPossible = property(get_values_possible, set_values_possible, del_values_possible, "when only specific values are possible")
	name = property(get_name, set_name, del_name, "When parameter is saved this will be the name in the file")
	listLen = property(get_list_len, set_list_len, del_list_len, "listLen's use only when tatatyp==list")
	disabled = property(get_disabled, set_disabled, del_disabled, "When a property should be disabled by default, set this property on True")

	
			