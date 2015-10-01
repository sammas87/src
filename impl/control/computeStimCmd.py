'''
Created on 26.09.2015

@author: schneidersmatthias
'''
def computeStimCmdChannel(channelNr,mA,pulseWith):
    sof=[255,255]
    databytesCount=4;
    cmdNr=1
    if (channelNr<1 or channelNr >8):
        print('channelNr: '+str(channelNr)+" must be between 1-8 ")
        return
    if(mA<0 or mA>125):
        print('mA: ' + str(mA) + ' must be between 0 and 125 ')
        return
    else:
        mAc=mA
    if(pulseWith<0 or pulseWith>500):
        print('pulseWith: ' + str(pulseWith) + ' must be between 0 and 500us ')
        return
    else:
        pulseWithC=[0, 0]
        if(pulseWith>256):
            pulseWithC[0]=1
            pulseWith=pulseWith-256
        pulseWithC[1]=pulseWith;
    checksum=sum([databytesCount,cmdNr,channelNr,mAc,pulseWithC[0],pulseWithC[1]])%256    
    cmd=[sof[0],sof[1],databytesCount,cmdNr,channelNr,mAc,pulseWithC[0],pulseWithC[1],checksum]
    return cmd
def computeCmdStimulationFrequenzChannel(channelNr,hz):
    sof=[255,255]
    databytesCount=2;
    cmdNr=3
    if (channelNr<1 or channelNr >8):
        print('channelNr: '+str(channelNr)+" must be between 1-8 ")
        return
    if(hz<1 or hz>99):
        print('Stimfrequenz: '+str(hz)+" must be between  1-99")
        return
    checksum=sum([databytesCount,cmdNr,channelNr,hz])%256    
    cmd=[sof[0],sof[1],databytesCount,cmdNr,channelNr,hz,checksum]
    return cmd
def computeCmdStimulationFrequenzGlobal(hz):
    sof=[255,255]
    databytesCount=1;
    cmdNr=2
    if(hz<1 or hz>99):
        print('Stimfrequenz: '+str(hz)+" must be between  1-99")
        return
    checksum=sum([databytesCount,cmdNr,hz])%256    
    cmd=[sof[0],sof[1],databytesCount,cmdNr,hz,checksum]
    return cmd
