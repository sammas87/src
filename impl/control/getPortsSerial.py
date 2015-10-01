# -*- coding: iso-8859-15 -*-
'''
Created on 21.08.2015

@author: schneidersmatthias
'''
import serial.tools.list_ports
import sys
def getPortNrAnsteuerung():
    usbToSerial='Serial On USB'
    arduino='Arduino'
    portSerialToUSB=-1
    portArduino=-1
    pportSerialToUSB=-1
    pportArduino=-1
    ports = list(serial.tools.list_ports.comports())
    nr=0
    
    for p in ports:
        print p
        print p[0]
        print p[1]
        print p[2]
        if p[1].__len__()>=len(arduino) and p[1][0:len(arduino)]==arduino:
            portArduino=int(p[0][3:len(p[0])])
            pportArduino=nr
        if p[1].__len__()>=len(usbToSerial) and p[1][0:len(usbToSerial)]==usbToSerial :
            portSerialToUSB=int(p[0][3:len(p[0])])
            pportSerialToUSB=nr
        print "\n\n"
        nr=nr+1

    
    if (portSerialToUSB>=0 and portArduino>=0):
        print 'Erfolgreich ports gefunden!'
        print ports[pportSerialToUSB][1] + ' COM:' + str(portSerialToUSB)
        print ports[pportArduino][1] + ' COM:' + str(portArduino)
    else:
        print 'Die Portbelegung konnte nicht automatisch vom System übernommen werden!'
        print 'Bitte die Portnr für das FES-Modul eingeben: '
        portSerialToUSB=int(sys.stdin.readline())
        print 'Bitte die Portnr für die Elektrodenasteuerung eingeben: '
        portArduino=int(sys.stdin.readline())
        print 'Konfiguration: FES:' + str(portSerialToUSB) +" und Elektrodenansteuerung: " + str(portArduino) + ' übernommen'
    
    return portSerialToUSB-1, portArduino-1

#if __name__ == "__main__":
#    portSerialToUSB, portArduino=getPortNrAnsteuerung()
#    print 'Konfiguration: COM-FES:' + str(portSerialToUSB) +" und COM-lektrodenansteuerung: " + str(portArduino) + ' übernommen'