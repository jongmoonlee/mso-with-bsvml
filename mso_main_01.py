#############################################################
###########  GUI FRONT PANEL ################################

import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
from itertools import chain
import bs_machine_bsvml
import configparser

timer = QtCore.QTimer()
config = configparser.ConfigParser()
config.read('BSConfig.ini')
bs_machine_bsvml.userParam.update({"BufferSize": int(config['DEFAULT']['BufferSize'])})

class Window(QtGui.QTabWidget):
    EXIT_CODE_REBOOT = -123
    '''user settings'''    

    def __init__(self, parent = None):
        # global connectedBS
        super(Window, self).__init__(parent)
        self.setGeometry(int(config['DEFAULT']['GeomPosX']), \
            int(config['DEFAULT']['GeomPosY']) , \
            int(config['DEFAULT']['GeomWidth']), \
            int(config['DEFAULT']['GeomLength']))
            
        self.tab1 =  QtGui.QWidget()
        self.tab2 =  QtGui.QWidget()
        self.tab3 =  QtGui.QWidget()
        self.tab4 =  QtGui.QWidget()
            
        self.addTab(self.tab1,"Streaming")
        self.addTab(self.tab2,"QuadChs")
        self.addTab(self.tab3,"WaveGen")
        self.addTab(self.tab4,"Decode+")

        self.setWindowTitle("BitScope MSO")
        self.setWindowIcon(QtGui.QIcon('./Images/BitScope.png'))
        self.tab1UI()    
        self.plotList=[]   
        self.plotNameList=[]        
        self.setzone = int(config['DEFAULT']['SetZone']) 
        self.sample = int(config['DEFAULT']['PlotSample']) 
        self.target = 0
        self.zoomTarget = len(self.plotList)-1
        self.isDual = False
        self.isLogic = False 
        self.isRunning = False    
        self.isInitialRunExecuted = False
        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)
        

    def tab1UI(self):
        layout = QtGui.QGridLayout() 
        layout.setHorizontalSpacing(2)
        
        """Layout widget definition"""
        self.win = pg.GraphicsLayoutWidget()
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)
        self.tab1.setLayout(layout)   

        """generate Components"""
        self.comboBoxCOM = QtGui.QComboBox()
        self.comboBoxCOM.addItems(bs_machine_bsvml.findBS())
        self.comboBoxCOM.setStyleSheet('QComboBox {background-color: white; color:black;}')
        
        self.btnRunning = QtGui.QPushButton("", self)      
        self.btnRunning.setCheckable(True)
        self.btnRunning.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        
        self.btnRunning.setStyleSheet('QPushButton {background: transparent}')
        self.btnRunning.setIcon(QtGui.QIcon('./Images/ledOFF.jpeg'))
        self.btnRunning.clicked.connect(self.running)

        # mode (do not change names)
        self.comboBoxMode = QtGui.QComboBox()
        self.comboBoxMode.addItem("Please Select")
        self.comboBoxMode.addItems(["Dual","Mixed","SingleFast","SingleMacro","DualMacro"])
        self.comboBoxMode.setStyleSheet('QComboBox {background-color: white}')
        self.comboBoxMode.currentIndexChanged.connect(self.modebtnPressed) 
        
        # CHA and CHB
        self.btnChA = QtGui.QPushButton("CHA", self)  
        self.btnChA.setStyleSheet('QPushButton {background-color: yellow; color:black;}')
        self.btnChA.setCheckable(True)
        self.btnChA.setEnabled(False)          
        self.btnChA.clicked[bool].connect(self.btnChAPressed)
        self.btnChB = QtGui.QPushButton("CHB", self)
        self.btnChB.setStyleSheet('QPushButton {background-color: green; color:white}')
        self.btnChB.setCheckable(True)
        self.btnChB.setEnabled(False)
        self.btnChB.setChecked(False) 
        self.btnChB.clicked[bool].connect(self.btnChBPressed)

        # Logic: Forget about iteration.. what's 'for'?
        self.btnL0 = QtGui.QPushButton("L0",self)
        self.btnL1 = QtGui.QPushButton("L1",self)  
        self.btnL2 = QtGui.QPushButton("L2",self)  
        self.btnL3 = QtGui.QPushButton("L3",self)  
        self.btnL4 = QtGui.QPushButton("L4",self)          
        self.btnL5 = QtGui.QPushButton("L5",self)  
        self.btnL6 = QtGui.QPushButton("L6",self)  
        self.btnL7 = QtGui.QPushButton("L7",self)
        
        # too many logic buttons
        self.btnL0.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        self.btnL1.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        self.btnL2.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        self.btnL3.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        self.btnL4.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        self.btnL5.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        self.btnL6.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))
        self.btnL7.setFixedWidth(int(config['DEFAULT']['LogicBtnWidth']))

        self.btnL0.setCheckable(True)
        self.btnL0.toggle()  
        self.btnL0.setChecked(False)
        self.btnL0.setEnabled(False)        
        self.btnL0.clicked.connect(self.buttonPressed)

        self.btnL1.setCheckable(True)
        self.btnL1.toggle()  
        self.btnL1.setChecked(False)
        self.btnL1.setEnabled(False)        
        self.btnL1.clicked.connect(self.buttonPressed)

        self.btnL2.setCheckable(True)
        self.btnL2.toggle()  
        self.btnL2.setChecked(False)
        self.btnL2.setEnabled(False)        
        self.btnL2.clicked.connect(self.buttonPressed)

        self.btnL3.setCheckable(True)
        self.btnL3.toggle()  
        self.btnL3.setChecked(False) 
        self.btnL3.setEnabled(False)       
        self.btnL3.clicked.connect(self.buttonPressed)
        
        self.btnL4.setCheckable(True)
        self.btnL4.toggle()  
        self.btnL4.setChecked(False)  
        self.btnL4.setEnabled(False)      
        self.btnL4.clicked.connect(self.buttonPressed)

        self.btnL5.setCheckable(True)
        self.btnL5.toggle()  
        self.btnL5.setChecked(False) 
        self.btnL5.setEnabled(False)       
        self.btnL5.clicked.connect(self.buttonPressed)

        self.btnL6.setCheckable(True)
        self.btnL6.toggle()  
        self.btnL6.setChecked(False) 
        self.btnL6.setEnabled(False)       
        self.btnL6.clicked.connect(self.buttonPressed)

        self.btnL7.setCheckable(True)
        self.btnL7.toggle()  
        self.btnL7.setChecked(False)
        self.btnL7.setEnabled(False)        
        self.btnL7.clicked.connect(self.buttonPressed)

        self.btnL0.setStyleSheet('QPushButton {background-color: purple; color:white}')
        self.btnL1.setStyleSheet('QPushButton {background-color: blue; color:white}')
        self.btnL2.setStyleSheet('QPushButton {background-color: cyan; color:black}')
        self.btnL3.setStyleSheet('QPushButton {background-color: magenta; color:black}')
        self.btnL4.setStyleSheet('QPushButton {background-color: orange; color:black}')
        self.btnL5.setStyleSheet('QPushButton {background-color: red; color:black}')
        self.btnL6.setStyleSheet('QPushButton {background-color: brown; color:black}')
        self.btnL7.setStyleSheet('QPushButton {background-color: grey; color:black}')
    
        #Sample rate
        self.samplerateLabel = QtGui.QLabel("   Clock setting",self)
        self.dialSR = QtGui.QDial(self)
        self.dialSR.setNotchesVisible(True)
        self.dialSR.setMinimum(int(config['DEFAULT']['SampleRateMin']))
        self.dialSR.setMaximum(int(config['DEFAULT']['SampleRateMax']))
        self.spinSR = QtGui.QSpinBox()   
        self.spinSR.setMinimum(int(config['DEFAULT']['SampleRateMin']))
        self.spinSR.setMaximum(int(config['DEFAULT']['SampleRateMax']))     
        self.dialSR.valueChanged.connect(self.spinSR.setValue)
        self.spinSR.valueChanged.connect(self.dialSR.setValue)
        self.spinSR.valueChanged.connect(self.buttonPressed)
        
        #Duration
        self.durationLabel = QtGui.QLabel(" Duration [sec]",self)
        self.dialDuration = QtGui.QDial()
        self.dialDuration.setNotchesVisible(True)
        self.spinDuration = QtGui.QSpinBox()   
        self.dialDuration.setMinimum(int(config['DEFAULT']['DurationMin']))
        self.dialDuration.setMaximum(int(config['DEFAULT']['DurationMax']))
        self.spinDuration.setMinimum(int(config['DEFAULT']['DurationMin']))
        self.spinDuration.setMaximum(int(config['DEFAULT']['DurationMax']))     
        self.dialDuration.valueChanged.connect(self.spinDuration.setValue)
        self.spinDuration.valueChanged.connect(self.dialDuration.setValue)
        self.spinDuration.valueChanged.connect(self.buttonPressed)
        
        self.spinDuration.setMinimum(int(config['DEFAULT']['DurationMin']))
        self.spinDuration.setMaximum(int(config['DEFAULT']['DurationMax']))
        #Buttons
        self.btnTest = QtGui.QPushButton("STOP", self)  
        self.btnTest.setCheckable(True)
        self.btnTest.toggle()  
        self.btnTest.setEnabled(True)  
        self.btnTest.clicked.connect(self.stopTest)
        # Start,Stop,Reset
        self.btnStart = QtGui.QPushButton("START", self)
        self.btnStart.setEnabled(False)
        self.btnStart.clicked[bool].connect(self.startBtnPressed) 


        self.btnFrameUpdate = QtGui.QPushButton("CONT_ON", self)
        self.btnFrameUpdate.setCheckable(True)  
        self.btnFrameUpdate.setEnabled(False)
        self.btnFrameUpdate.clicked[bool].connect(self.timerToggle)
        self.btnRst = QtGui.QPushButton("RESET", self)
        self.btnRst.setCheckable(True)
        self.btnRst.setEnabled(False)
        self.btnRst.clicked[bool].connect(self.resetAll)
        self.btnUpdate = QtGui.QPushButton("UPDATE", self)
        self.btnUpdate.setEnabled(False)
        self.btnUpdate.setCheckable(True)
        self.btnUpdate.clicked.connect(self.updatePlot)

        # Toggle, Quit
        self.btnToggle = QtGui.QPushButton("TOGGLE", self)
        self.btnToggle.setCheckable(True)
        self.btnToggle.setEnabled(False)        
        self.btnToggle.clicked.connect(self.buttonToggle)
        
        self.btnQuit = QtGui.QPushButton("QUIT", self)
        self.btnQuit.clicked.connect(QtCore.QCoreApplication.instance().quit)  
        self.status = QtGui.QListWidget()
        self.status.setStyleSheet('QListWidget {font-size: 10px}')
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setStyleSheet('QProgressBar::chunk {background-color: #7799AA}')
        # Layout management
        #COMport and Macro
        layout.addWidget(self.comboBoxMode,1,2,1,7) 
        layout.addWidget(self.btnRunning,1,1,1,1)
        layout.addWidget(self.comboBoxCOM,2,1,1,4) 
        #Mode
        layout.addWidget(self.btnTest,2,5,1,4)
        #Row3: CHA and CHB
        layout.addWidget(self.btnChA,3,1,1,4 )        
        layout.addWidget(self.btnChB,3,5,1,4 )
        #Logic
        layout.addWidget(self.btnL0,4,1,1,1)  
        layout.addWidget(self.btnL1,4,2,1,1)    
        layout.addWidget(self.btnL2,4,3,1,1)   
        layout.addWidget(self.btnL3,4,4,1,1)   
        layout.addWidget(self.btnL4,4,5,1,1)   
        layout.addWidget(self.btnL5,4,6,1,1)   
        layout.addWidget(self.btnL6,4,7,1,1)   
        layout.addWidget(self.btnL7,4,8,1,1)    

        #dials: Sample rate and buffer size Display
        layout.addWidget(self.samplerateLabel,5,1,1,4)
        layout.addWidget(self.durationLabel,5,5,1,4)
        #Sample rate and BufferSize
        layout.addWidget(self.dialSR,6,1,1,4)
        layout.addWidget(self.dialDuration,6,5,1,4)
      
        layout.addWidget(self.spinSR,7,1,1,4) 
        layout.addWidget(self.spinDuration,7,5,1,4)

        #START, STOP, RESET
        layout.addWidget(self.btnStart,8,1,1,4)
        layout.addWidget(self.btnFrameUpdate,8,5,1,4)
        layout.addWidget(self.btnRst,9,1,1,4)
        layout.addWidget(self.btnUpdate,9,5,1,4)

        layout.addWidget(self.btnToggle,10,1,1,4)  
        layout.addWidget(self.btnQuit,10,5,1,4)        

        layout.addWidget(self.status,11,1,2,8)
        layout.addWidget(self.win,1,0,12,1)
        
        layout.addWidget(self.progressBar,13,0,1,9)
        # self.show()    

#############################################################
###########  USER EVENT HANDLERS ############################

    def btnChAPressed(self):
        self.status.clear()
        self.stop() if  self.isRunning else None
        self.resetAll() if  self.isRunning else None

        mode = self.comboBoxMode.currentText()
        self.status.addItem("Running in "+ str(mode))

        self.plotNameList = []
        if mode.startswith("Single"):           
            self.btnChB.toggle() 
            bs_machine_bsvml.userParam.update({"isDual":False})
            bs_machine_bsvml.userParam.update({"CHA":True})
            bs_machine_bsvml.userParam.update({"CHB":False}) 
        else:
            print('else')
        self.status.addItem("CHA added") 
        self.plotNameList.append("CHA") 

    
    def btnChBPressed(self):
        self.status.clear()
        self.stop() if  self.isRunning else None
        self.resetAll() if  self.isRunning else None
        mode = self.comboBoxMode.currentText()
        self.status.addItem("Running in "+ str(mode))

        self.plotNameList = []
        if mode.startswith("Single"):           
            self.btnChA.toggle() 
            bs_machine_bsvml.userParam.update({"isDual":False})
            bs_machine_bsvml.userParam.update({"CHA":False})
            bs_machine_bsvml.userParam.update({"CHB":True}) 
        else:
            print('else')
        self.status.addItem("CHB added")  
        self.plotNameList.append("CHB") 

    def modebtnPressed(self):
        print('mode btn pressed')
        mode = str(self.comboBoxMode.currentText())
        bs_machine_bsvml.userParam.update({"testMode":mode})

        self.status.clear()
        self.stop() if  self.isRunning else None
        self.resetAll() if  self.isRunning else None
    
        self.btnFrameUpdate.setEnabled(True)
        self.btnRst.setEnabled(True)
        self.btnToggle.setEnabled(True)       
        self.btnChA.setEnabled(True)
        self.btnChB.setEnabled(True)   

        
        if mode == "Dual" or mode=="Mixed":
            self.status.clear() 
            self.plotNameList= []
            self.btnChA.setCheckable(True)
            self.btnChB.setCheckable(True)
            self.btnChA.toggle() if not self.btnChA.isChecked() else None
            self.btnChB.toggle() if not self.btnChB.isChecked() else None 

            self.plotNameList.append("CHA")
            self.plotNameList.append("CHB")

            self.status.addItem("Running in " + mode + " mode") 
            self.status.addItem(str(self.plotNameList)) 
            bs_machine_bsvml.userParam.update({"isDual":True})
            bs_machine_bsvml.userParam.update({"CHA":True})
            bs_machine_bsvml.userParam.update({"CHB":True})

            self.btnL0.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L0": False})
            self.btnL1.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L1": False})
            self.btnL2.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L2": False})
            self.btnL3.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L3": False})
            self.btnL4.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L4": False})
            self.btnL5.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L5": False})
            self.btnL6.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L6": False})
            self.btnL7.setEnabled(True) if mode.startswith("Mixed") else bs_machine_bsvml.userParam.update({"L7": False})

            self.btnL0.toggle() if self.btnL0.isChecked() else None
            self.btnL1.toggle() if self.btnL1.isChecked() else None
            self.btnL2.toggle() if self.btnL2.isChecked() else None
            self.btnL3.toggle() if self.btnL3.isChecked() else None
            self.btnL4.toggle() if self.btnL4.isChecked() else None
            self.btnL5.toggle() if self.btnL5.isChecked() else None
            self.btnL6.toggle() if self.btnL6.isChecked() else None
            self.btnL7.toggle() if self.btnL7.isChecked() else None

            self.dialSR.setMinimum(int(config['DEFAULT']['DualMin']))
            self.spinSR.setMinimum(int(config['DEFAULT']['DualMin']))
            
 

        elif mode == "SingleFast":
            self.status.clear() 
            self.plotNameList= []
            self.status.addItem("Running in " + mode + " mode") 
            if not self.btnChA.isChecked():
                self.btnChA.toggle()
                self.plotNameList.append("CHA")
                bs_machine_bsvml.userParam.update({"isDual":False})
                bs_machine_bsvml.userParam.update({"CHA":True})
                bs_machine_bsvml.userParam.update({"CHB":False})                
                self.status.addItem(str(self.plotNameList))
                self.btnChB.toggle() if self.btnChB.isChecked() else None
            else:
                self.btnChB.toggle()
                self.plotNameList.append("CHB")   
                bs_machine_bsvml.userParam.update({"isDual":False})
                bs_machine_bsvml.userParam.update({"CHA":False})
                bs_machine_bsvml.userParam.update({"CHB":True})              
                self.status.addItem(str(self.plotNameList))
                self.btnChA.toggle() if self.btnChA.isChecked() else None
            self.dialSR.setMinimum(int(config['DEFAULT']['SingleFastMin']))
            self.spinSR.setMinimum(int(config['DEFAULT']['SingleFastMin'])) 
        elif mode == "SingleMacro":  
            print(mode,"single mode selected")
            self.dialSR.setMinimum(int(config['DEFAULT']['SingleMacroMin']))
            self.spinSR.setMinimum(int(config['DEFAULT']['SingleMacroMin'])) 
        else:
            self.dialSR.setMinimum(int(config['DEFAULT']['DualMacroMin']))
            self.spinSR.setMinimum(int(config['DEFAULT']['DualMacroMin']))            
        self.btnStart.setEnabled(True)
           

    def buttonPressed(self): 

        mode = str(self.comboBoxMode.currentText())
        bs_machine_bsvml.userParam.update({"testMode":mode})

        self.stop() if  self.isRunning else None
        self.resetAll() if  self.isRunning else None
       
        self.btnTest.setEnabled(True)
        self.btnFrameUpdate.setEnabled(False)

        if bs_machine_bsvml.userParam["testMode"] == "Mixed":
            self.status.addItem("L0 added") if self.btnL0.isChecked() else None
            self.status.addItem("L1 added") if self.btnL1.isChecked() else None
            self.status.addItem("L2 added") if self.btnL2.isChecked() else None
            self.status.addItem("L3 added") if self.btnL3.isChecked() else None
            self.status.addItem("L4 added") if self.btnL4.isChecked() else None
            self.status.addItem("L5 added") if self.btnL5.isChecked() else None
            self.status.addItem("L6 added") if self.btnL6.isChecked() else None
            self.status.addItem("L7 added") if self.btnL7.isChecked() else None                         
        
            self.plotNameList.append("L0") if self.btnL0.isChecked() else None
            self.plotNameList.append("L1") if self.btnL1.isChecked() else None
            self.plotNameList.append("L2") if self.btnL2.isChecked() else None
            self.plotNameList.append("L3") if self.btnL3.isChecked() else None
            self.plotNameList.append("L4") if self.btnL4.isChecked() else None
            self.plotNameList.append("L5") if self.btnL5.isChecked() else None
            self.plotNameList.append("L6") if self.btnL6.isChecked() else None
            self.plotNameList.append("L7") if self.btnL7.isChecked() else None    

            bs_machine_bsvml.userParam.update({"L0": True}) if self.btnL0.isChecked() else bs_machine_bsvml.userParam.update({"L0": False})
            bs_machine_bsvml.userParam.update({"L1": True}) if self.btnL1.isChecked() else bs_machine_bsvml.userParam.update({"L1": False})
            bs_machine_bsvml.userParam.update({"L2": True}) if self.btnL2.isChecked() else bs_machine_bsvml.userParam.update({"L2": False})
            bs_machine_bsvml.userParam.update({"L3": True}) if self.btnL3.isChecked() else bs_machine_bsvml.userParam.update({"L3": False})
            bs_machine_bsvml.userParam.update({"L4": True}) if self.btnL4.isChecked() else bs_machine_bsvml.userParam.update({"L4": False})
            bs_machine_bsvml.userParam.update({"L5": True}) if self.btnL5.isChecked() else bs_machine_bsvml.userParam.update({"L5": False})
            bs_machine_bsvml.userParam.update({"L6": True}) if self.btnL6.isChecked() else bs_machine_bsvml.userParam.update({"L6": False})
            bs_machine_bsvml.userParam.update({"L7": True}) if self.btnL7.isChecked() else bs_machine_bsvml.userParam.update({"L7": False})           

            self.btnStart.setEnabled(True)

        
    def buttonToggle(self):
        self.togglePlot() 
       
    def updateUserParam(self):
        self.plotNameList=[]
        self.plotNameList.append("CHA") if bs_machine_bsvml.userParam["CHA"] else None
        self.plotNameList.append("CHB") if bs_machine_bsvml.userParam["CHB"] else None
        self.plotNameList.append("L0") if bs_machine_bsvml.userParam["L0"] else None
        self.plotNameList.append("L1") if bs_machine_bsvml.userParam["L1"] else None
        self.plotNameList.append("L2") if bs_machine_bsvml.userParam["L2"] else None
        self.plotNameList.append("L3") if bs_machine_bsvml.userParam["L3"] else None
        self.plotNameList.append("L4") if bs_machine_bsvml.userParam["L4"] else None
        self.plotNameList.append("L5") if bs_machine_bsvml.userParam["L5"] else None
        self.plotNameList.append("L6") if bs_machine_bsvml.userParam["L6"] else None
        self.plotNameList.append("L7") if bs_machine_bsvml.userParam["L7"] else None
        self.status.addItem(str(self.plotNameList))
        self.plotNameList.append("Navigator")

        print('plotNameList', self.plotNameList)
        sampleRate = self.spinSR.value()
        bs_machine_bsvml.userParam.update({"sampleRate":sampleRate})
        duartion = self.spinDuration.value()
        bs_machine_bsvml.userParam.update({"duration":duartion})       

    def stop(self):
        bs_machine_bsvml.stopStreaming()        
        self.status.addItem('stream stopped')
        self.isRunning = False
        self.btnStart.setText("START")
        self.btnUpdate.setEnabled(False)
        self.btnRunning.setIcon(QtGui.QIcon('./Images/ledOFF.jpeg'))
    
    def quitApp(self):
        print('quit btn clicked')
        bs_machine_bsvml.serClose()
        QtCore.QCoreApplication.instance().quit

    def timerToggle(self):
        if self.btnFrameUpdate.text() == "CONT_ON":
            self.status.addItem('Cont_caputre with a frame rate: '+ (config['DEFAULT']['FrameRate'])+ "/s")
            self.btnFrameUpdate.setText('CONT_OFF')
            timer.timeout.connect(self.updatePlot)
            timer.start(int(config['DEFAULT']['FrameRate']))
        else:
            self.btnFrameUpdate.setText("CONT_ON")
            timer.stop()

    def stopTest(self): 
        print("test")
        self.stop() 
        

    def togglePlot(self):
        
        if self.target < len(self.plotList)-2:
            self.target = self.target +1
        else:
            self.target = 0

        self.setZoomRegion(len(self.plotNameList)-1)
        self.updatePlot() 
        self.setCrossUpdatePlot(self.target)

#############################################################
###########  PLOT HELPERS ###################################

    def setZoomRegion(self, zoom_target):
        #this should be the last element in the list      
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.plotList[zoom_target].addItem(self.region, ignoreBounds=True)

    #@@ in case of changing one that cross haired i.e.[1]
    def mouseMoved(self,evt):
        pos = evt[0]  
        if self.plotList[self.target].sceneBoundingRect().contains(pos):
            self.mousePoint = self.vb.mapSceneToView(pos)
            self.index = int(self.mousePoint.x())
            if self.index > 0 and self.index < self.sample:
                if bs_machine_bsvml.userParam["testMode"] == "Mixed":
                    self.label.setText("<span style='font-size: 9pt'>pt=%0.1f, \
                        <span style='color: yellow'>CHA=%0.1f</span>, \
                        <span style='color: green'>CHB=%0.1f</span> , \
                        <span style='color: blue'>Logic=%0.1f</span>" % \
                        (self.mousePoint.x(), self.plotData1[self.index], \
                        self.plotData2[self.index], self.plotData3[self.index])) 
                elif bs_machine_bsvml.userParam["testMode"][0:4] == "Dual":
                    self.label.setText("<span style='font-size: 9pt'>pt=%0.1f, \
                        <span style='color: yellow'>CHA=%0.1f</span>, \
                        <span style='color: green'>CHB=%0.1f</span>" % \
                        (self.mousePoint.x(), self.plotData1[self.index], self.plotData2[self.index])) 
                elif self.plotNameList[0] == "CHA":
                    self.label.setText("<span style='font-size: 9pt'>pt=%0.1f, \
                        <span style='color: yellow'>CHA=%0.1f</span>" % (self.mousePoint.x(), self.plotData1[self.index]))
                else:
                    self.label.setText("<span style='font-size: 9pt'>pt=%0.1f, \
                        <span style='color: green'>CHB=%0.1f</span>" % (self.mousePoint.x(), self.plotData1[self.index]))

            self.vLine.setPos(self.mousePoint.x())
            self.hLine.setPos(self.mousePoint.y())

   
   
    def update(self,target):
        self.region.setZValue(int(config['DEFAULT']['SetZValue']))
        minX, maxX = self.region.getRegion()
        self.plotList[self.target].setXRange(minX, maxX, padding=0)  

    def updateRegion(self,window, viewRange):
        rgn = viewRange[0] # do not touch
        self.region.setRegion(rgn)

    def setCrossUpdatePlot(self,target):
        # in case of changing one that cross haired i.e.[1]
        self.region.sigRegionChanged.connect(self.update)
        self.plotList[target].sigRangeChanged.connect(self.updateRegion)
        self.region.setRegion([10, self.setzone])

        # in case of changing one that cross haired i.e.[1]
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plotList[target].addItem(self.vLine, ignoreBounds=True)
        self.plotList[target].addItem(self.hLine, ignoreBounds=True)

        self.vb = self.plotList[target].vb
        self.proxy = pg.SignalProxy(self.plotList[target].scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def addPlot(self):
        self.resetAll()
        self.plotList =[]

        self.zoomTarget = len(self.plotNameList)-1

        for cnt in self.plotNameList:  
            self.plotList.append(pg.PlotItem())
           
        for cnt in range(len(self.plotList)):
            self.win.addItem(self.plotList[cnt],row=cnt+1, col=0)
        for cnt in range(len(self.plotList)-1):
            title = str(self.plotNameList[cnt])
            unit="V" if title.startswith("CH") else None
            self.plotList[cnt].setLabel('left', title, units=unit)
            self.plotList[cnt].showGrid(x=True,y=True)      
        self.plotList[self.zoomTarget].setLabel('left',"Navigator{"+str(self.plotList[self.target])+")")
        return self.plotList
     

    def running(self): 
        print("runningtest")
        self.stop()      

    def resetAll(self):
        # print('reset presesd',self.plotNameList) 
        if len(self.plotList) > 0:
            for cnt in range(len(self.plotList)):
                self.win.removeItem(self.plotList[cnt]) 
        self.plotList =[]    

    def setProgressbar(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.00001
            self.progressBar.setValue(self.completed)
 
    def findBS(self):
        self.comboBoxCOM.addItem(bs_machine_bsvml.userParam["BSModel1"])
    

    #############################################################
    ###########  CAPTURE AND PLOT ###############################

    def plotRealDual(self,data):   
      
        self.plotData1 = [] ; self.plotData2 = [] ; self.plotData3 = []

        if bs_machine_bsvml.userParam["testMode"]=="Mixed":  
            self.plotList[0].plot(data["chA"], pen='ye')
            self.plotList[1].plot(data["chB"], pen='g')
            self.plotList[2].plot(data["logic"], pen='pu')
            self.plotList[len(self.plotNameList)-1].plot(data["chA"], pen='ye')
            for cnt in data["chA"]:
                self.plotData1.append(cnt)
            for cnt in data["chB"]:
                self.plotData2.append(cnt)
            for cnt in data["logic"]:
                self.plotData3.append(cnt)

        elif bs_machine_bsvml.userParam["testMode"][0:4] == "Dual":
            for cnt in data["chA"]:
                self.plotData1.append(cnt)
            for cnt in data["chB"]:
                self.plotData2.append(cnt)
            self.plotList[0].plot(data["chA"], pen='ye')
            self.plotList[1].plot(data["chB"], pen='g')
            self.plotList[len(self.plotNameList)-1].plot(data["chA"], pen='ye')

          
        elif bs_machine_bsvml.userParam["testMode"][0:6] == "Single" and self.plotNameList[0]=="CHA":
            self.plotList[0].plot(data["chA"][int(config['DEFAULT']['RubbishSize']):], pen='ye')
            self.plotList[len(self.plotNameList)-1].plot(data["chA"][int(config['DEFAULT']['RubbishSize']):], pen='ye')
            for cnt in data["chA"]:
                self.plotData1.append(cnt)
        else:
            self.plotList[0].plot(data["chA"][int(config['DEFAULT']['RubbishSize']):], pen='g')
            self.plotList[len(self.plotNameList)-1].plot(data["chA"][int(config['DEFAULT']['RubbishSize']):], pen='g')
            for cnt in data["chA"]:
                self.plotData1.append(cnt)

          
        self.target = 0        
        self.setZoomRegion(len(self.plotNameList)-1) 
        colDict = {0:"yellow",1:"green",2:'purple',3:"blue",4:"cyan",5:'magenta', \
            6:"orange",7:"red",8:'brown',9:'grey'}
       
        self.setCrossUpdatePlot(self.target)
        self.plotList[self.zoomTarget].setLabel('left',"Navigator{"+str(self.plotNameList[self.target])+")")
  
###########  CAPTURE SIG AND UPDTE PLOT ###############################   
    def captureSigUpdatePlot(self):

        self.btnRst.setEnabled(True)
        self.addPlot()
        bs_machine_bsvml.setupBS() if self.isRunning == False else None
        bs_machine_bsvml.startStreaming() if self.isRunning == False else None
      
        if self.spinDuration.value()>0:
            ## Stream on during capture
            self.btnRunning.setIcon(QtGui.QIcon('./Images/ledON.jpeg')) 
            self.plotRealDual(bs_machine_bsvml.getStreamDual())
            self.btnRunning.setIcon(QtGui.QIcon('./Images/ledOFF.jpeg'))                
            self.btnStart.setText("START")  
            self.isRunning = False
            self.btnUpdate.setEnabled(False)
            self.btnFrameUpdate.setEnabled(False)
        else:
            ## Stream on while running
            self.plotRealDual(bs_machine_bsvml.getStreamFast(int(config['DEFAULT']['FastSampleSize'])))
            self.btnStart.setText("STOP")
            self.btnRunning.setIcon(QtGui.QIcon('./Images/ledON.jpeg'))
            self.isRunning = True
            self.btnUpdate.setEnabled(True)
            self.btnFrameUpdate.setEnabled(True)


    def updatePlot(self):

        # print('isRunning',self.isRunning)

        if self.isRunning:
            self.status.clear()
            self.status.addItem("plot updated!")
            self.btnRunning.setIcon(QtGui.QIcon('./Images/ledON.jpeg'))
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(0)
            self.progressBar.setValue(0)
            self.myLongTask.start()


            self.btnRst.setEnabled(True)
            self.addPlot()

            # DUAL CHANNEL CAPTURE
            if bs_machine_bsvml.userParam["isDual"]:
                ## DUAL CH wite NO Summary           
                self.plotRealDual(bs_machine_bsvml.getStreamFast(int(config['DEFAULT']['ToGetAtATime'])))
                self.btnRunning.setIcon(QtGui.QIcon('./Images/ledON.jpeg'))
                self.isRunning = True

            # SINGLE CHANNEL CAPTURE        
            else:            
                self.plotRealDual(bs_machine_bsvml.getStreamFast(int(config['DEFAULT']['ToGetAtATime'])))
                self.btnStart.setText("STOP")
                self.btnRunning.setIcon(QtGui.QIcon('./Images/ledON.jpeg'))
                self.isRunning = True
                
            self.status.addItem("Sample Rate: " + \
                "{0:.2f}".format((bs_machine_bsvml.summaryDict["sampleRate"])) + "Ksps")
            self.status.addItem("Total data points: " + \
                str(bs_machine_bsvml.summaryDict["dataPt"]) + " collected")
            self.status.addItem("ActualDuration: " + \
                "{0:.2f}".format(bs_machine_bsvml.summaryDict["actualDuration"]) + "s")
        else:
            self.status.clear()
            self.status.addItem("stream stopped!")

    ###########  START ##########################################

    def startBtnPressed(self, down):
        self.btnRunning.setIcon(QtGui.QIcon('./Images/ledON.jpeg'))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(0)
        self.myLongTask.start()

        print ("Start button clicked", self.plotNameList) 
        self.updateUserParam()       
        self.status.clear()

        if self.isInitialRunExecuted == False:
            # bs_machine_bsvml.connectBS()
            print("check")
        else:
            self.stop()
            self.isInitialRunExecuted = True
  
        if self.btnStart.text() == "START":   
            
            self.addPlot()                   
            self.captureSigUpdatePlot()

            self.status.addItem("Sample Rate: " + \
                "{0:.2f}".format((bs_machine_bsvml.summaryDict["sampleRate"])) + "Ksps")
            self.status.addItem("Total data points: " + \
                str(bs_machine_bsvml.summaryDict["dataPt"]) + " collected")
            self.status.addItem("ActualDuration: " + \
                "{0:.2f}".format(bs_machine_bsvml.summaryDict["actualDuration"]) + "s")
            self.status.addItem("BufferSize: " + str(bs_machine_bsvml.userParam["BufferSize"]/1000000)+"M")
            
            if bs_machine_bsvml.userParam["duration"]>0:
                self.btnStart.setText("START")
                self.btnFrameUpdate.setEnabled(False)
            else:
                self.btnStart.setText("STOP")
                self.btnFrameUpdate.setEnabled(True)

        else:
            self.stop()
            self.btnStart.setText("START") 
    
    def onStart(self): 
        self.startBtnPressed
        self.progressBar.setRange(0,0)
        self.myLongTask.start()

    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0,1)
        self.progressBar.setValue(1)

class TaskThread(QtCore.QThread):
    taskFinished = QtCore.pyqtSignal()
    def run(self):
        self.taskFinished.emit() 
   
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window() 
    GUI.show()
    QtGui.QApplication.instance().exec_()    
    sys.exit(app.exec_())

def showdialog():
   d = QtGui.QDialog()
   b1 = QtGui.QPushButton("OK",d)
   b1.move(50,50)
   d.setWindowTitle("NO BITSCOPE FOUND!!")
   d.setWindowModality(QtCore.Qt.ApplicationModal)
   d.exec_()

if __name__ == '__main__':
    run()