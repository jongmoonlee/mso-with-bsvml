#############################################################
###########  CAPTURE ENGINE  ################################
import time
import struct
import sys
from itertools import chain
import py_bsvml as bv
from ctypes import *

bs = 0 #test one device for now

# bitlink.BS_Init()
# fileName = "unpacked" + str(time.time())
# filePath = "./" + fileName + ".csv"
# dumpFile = open(filePath, "w")

#############################################################
######  GLOBAL VAR ##########################################
val =''
duration=3
serWaiting = 0
toGetatATime = 500
CHA = []; CHB= []

userParam = {"testMode":"", "isDual":False, "isLogic": False, \
    "CHA":False, "CHB": False, "sampleRate":0, "duration":0, \
    "toGet":0, "COM1":"","COM2":"","BSModel1":"","BSModel2":"", \
    "BufferSize": 0, \
    "L0":False,"L1":False,"L2":False,"L3":False,"L4":False,"L5":False,"L6":False,"L7":False  }

summaryDict = {"dataPt":0, "actualDuration":0, "sample_rate":0}


#############################################################
######  FIND BITSCOPE #######################################

def findBS():
    bsInfo = (bv.BitScopeInfo*10)()
    bsCount = bv.listBitScopes(10, bsInfo)
    
    connectedBS=[]
    for cnt in range(bsCount):
        tempStr = str(bsInfo[cnt].model).strip('b').strip("'")
        print(type(tempStr))
        bv.openBitScope(bsInfo[0].port)
        connectedBS.append(tempStr)
    return connectedBS

#############################################################
###### SETTINGS FROM FRONT PANEL ############################
  
def setupBS():
    print('setUpBS started')
    print(userParam)

    bv.mode(bs, bv.STREAM_SINGLE)
    bv.enableAnalogueChannel(bs, bv.CHA)
    bv.rate(bs, (userParam["sampleRate"]))
    bv.dumpSize(bs, 2000)
    bv.range(bs, 5) # v
    bv.offset(bs, 1) # v
    bv.updateBitScope(bs)

#############################################################
###### SERIAL HELPERS #######################################
def writeToFile(file, data):
    # Write to file
    dataStr = '\n'.join(map(str, data))
    toWrite = dataStr + '\n'
    file.write(toWrite)


#############################################################
###### STREAMING ############################################

def startStreaming():
    print('strm started')  
    startTime = float(time.time())
    bv.stream(bs)
    return startTime

def stopStreaming():
    print('strm stoppend')
    bv.cancel(bs)
    bv.updateBitScope(bs)
    stopTime = float(time.time())
    return stopTime


def streamDataDual(startTime, duration):
    duration=duration
    state = True
    i = 0
    chAA =[]; chBB= []; logicC =[]

    bv.dumpSize(bs, toGetatATime)
    bv.updateBitScope(bs)
    while state:
        if (time.time()-startTime> duration) or (toGetatATime*i>1000000):
            print('strttime',startTime)
            state = False
        data = (c_ubyte * toGetatATime)()     

        bv.streamAcquire(bs, data)
        # bv.splitDualStream(data, chAA, chBB, bytes, False)

        if userParam["testMode"][0:6] == "Single":
            chA = (data)
            chAA.append(chA)
            print('')
        elif userParam["testMode"][0:4]=="Dual":
            # chA,chB = decodeChannel(data)
            # chAA.append(chA)
            # chBB.append(chB)
            print('')
        else:
            # chA,chB,logic = decodeChannel(data)
            # chDict ={"chA":chA, "chB":chB, "logic":logic}
            # chAA.append(chA)
            # chBB.append(chB)
            # logicC.append(logic)
            print('')
        i = i + 1
   
    if userParam["testMode"]=="Mixed":
        chDict ={"chA":list(chain(*chAA)), "chB":list(chain(*chBB)), "logic":list(chain(*logicC))} 
    elif userParam["testMode"][0:4]=="Dual":
        chDict ={"chA":list(chain(*chAA)), "chB":list(chain(*chBB))}  
    else:
        chDict ={"chA":list(chain(*chAA)), "chB":list(chain(*chBB))}  
    return chDict
    


def getStreamFast(sample):
    startTime = time.time()
    

    data = (c_ubyte * 2000)() # set size of unsigned char array

    time.sleep(0.1)

    bv.streamAcquire(bs, data)
    
    chA = (data)
    chB = (data)
    chDict ={"chA":chA, "chB":chB}

    actualDuration = (time.time()-startTime)
    sampleRate = 0
    summaryDict.update({"dataPt": len(chDict["chA"]), "actualDuration": actualDuration,"sampleRate": sampleRate})
    return chDict

def getStreamDual():
    startTime = time.time()
    results = (streamDataDual(startTime,userParam["duration"]))
    stopStreaming()
    actualDuration = time.time()-startTime
    sampleRate = (len(results["chA"]))/actualDuration/1000
    summaryDict.update({"dataPt": len(results["chA"]), "actualDuration": actualDuration,"sampleRate": sampleRate})
    return results
   

def main2():
    findBS()

if __name__ == '__main__':
    main2()
