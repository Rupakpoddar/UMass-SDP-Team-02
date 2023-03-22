import qwiic_proximity
import qwiic_tca9548a
import time
import serial

myMux = qwiic_tca9548a.QwiicTCA9548A()
ports = [2, 3, 0, 4, 7]
proxValue1, proxValue2, proxValue3, proxValue4, proxValue5 = 0, 0, 0, 0, 0		#f, rf, rb, lf, lb
values = [proxValue1, proxValue2, proxValue3, proxValue4, proxValue5]

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

f_speed = 30
t_speed = 20
l_limit = 50
r_limit = 50	
f_limit = 30
p_error = 0.05
"""
def setup():
    print("Starting...")
    myMux.enable_channels
    BluetoothModule.init(9600, read_buf_len=64)
    Wire = I2C(1, I2C.MASTER, baudrate=9600)
    pyb.Pin("D13", pyb.Pin.OUT_PP)

    if myMux.connected() == False:
        print("Mux not detected. Freezing...")
        while True:
            pyb.LED(1).toggle()
            pyb.delay(1000)
"""

def loop(arg):
    global readString, lastCommand, command

    while(True):
        readString = input("give command ")
        
        if len(readString) > 0:
            print(readString)
            ser.write(readString.encode('utf-8'))
            lastCommand = readString
        
        if lastCommand != "s":
            command = lastCommand[3:]
            if (command == "left") or (command == "right") or (command == "br") or (command == "bl"):
                autoAlign(command)
                autoOrient(command)
            else:
                obstacleAvoidance()

def obstacleAvoidance():
    global command, values
    obstacleAvoidanceHelper()

    if command == "f":
        if values[1] > f_limit:
            print("s")
            ser.write("s".encode('utf-8'))
            command = ""
    
    # if command == "b":
    #     if values[?] > 30:
    #         print("s")
    #         CustomPCB.write("s".encode('utf-8'))
    #         command = ""

    if command == "l":
        if (values[3] > l_limit) or (values[4] > l_limit):
            print("s")
            ser.write("s".encode('utf-8'))
            command = ""
    if command == "r":
        if (values[0] > r_limit) or (values[2] > r_limit):
            print("s")
            ser.write("s".encode('utf-8'))
            command = ""

def obstacleAvoidanceHelper():
    global command, values
    y = 0
    while(y < 100):
        for i in range(5):
            myMux.enable_channels(ports[i])
            prox = qwiic_proximity.QwiicProximity()
            prox.begin()
            values[i] = prox.get_proximity()
            print(str(values[i]) + "\t", end="")
            myMux.disable_channels(ports[i])
        print("\n")
        y+=1
        #time.sleep()

def autoAlign(side):
    global lflow, lfhigh, lblow, lbhigh, rflow, rfhigh, rblow, rbhigh, values
    autoAlignHelper(side)
    if side == "left":
        while values[4] < lflow or values[4] > lfhigh:
            print(str(lflow) + "\t" + str(values[4]) + "\t" + str(lfhigh))
            autoAlignHelper(side)
            if values[4] < lflow:
                time.sleep(0.1)
                #ser.write("030cw".encode('utf-8'))
                print("cwing")
            if values[4] > lfhigh:
                time.sleep(0.1)
                #ser.write("030aw".encode('utf-8'))
                print("awing")
            
        time.sleep(0.1)
        print(str(lflow) + "\t" + str(values[4]) + "\t" + str(lfhigh))
        
    elif side == "right":
        while values[2] < rflow or values[2] > rfhigh:
            print(str(rflow) + "\t" + str(values[2]) + "\t" + str(rfhigh))
            autoAlignHelper(side)
            if values[2] < rflow:
                time.sleep(0.1)
                #ser.write("030cw".encode('utf-8'))
                print("cwing")
            if values[2] > rfhigh:
                time.sleep(0.1)
                #ser.write("030aw".encode('utf-8'))
                print("awing")
        time.sleep(0.1)
        print(str(rflow) + "\t" + str(values[2]) + "\t" + str(rfhigh))
        
        
    ser.write("s".encode('utf-8'))

def autoAlignHelper(side):
    global lflow, lfhigh, lblow, lbhigh, rflow, rfhigh, rblow, rbhigh, values 
    
    if side == "left":
        #get left front
        myMux.enable_channels(ports[3])
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
            
        values[3] = prox.get_proximity()
        lflow = values[3] - (values[3]*p_error)
        lfhigh = values[3] + (values[3]*p_error)
        myMux.disable_channels(ports[3])
        # print(str(values[3]) + "\t", end="")
        
        # get left back
        myMux.enable_channels(ports[4])
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
            
        values[4] = prox.get_proximity()
        lblow = values[4] - (values[4]*p_error)
        lbhigh = values[4] + (values[4]*p_error)
        myMux.disable_channels(ports[4])
        # print(str(values[4]))
        
    elif side == "right":
        # get right front 
        myMux.enable_channels(ports[1])
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
            
        values[1] = prox.get_proximity()
        rflow = values[1] - (values[1]*p_error)
        rfhigh = values[1] + (values[1]*p_error)
        myMux.disable_channels(ports[1])
        # print(str(values[3]) + "\t", end="")
        
        # get right back
        myMux.enable_channels(ports[2])
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
            
        values[2] = prox.get_proximity()
        rblow = values[2] - (values[2]*p_error)
        rbhigh = values[2] + (values[2]*p_error)
        myMux.disable_channels(ports[2])
        
def autoOrient(side):
    global values 
    
    if side == "left":
        while values[3] > l_limit:
            autoOrientHelper(side)
            comm = str(t_speed) + "cr"	# crabwalk right
            print(values[3], l_limit, values[4])
            #ser.write(comm.encode('utf-8'))
        myMux.disable_channels(ports[3])
    if side == "right":
        while values[1] > r_limit:
            autoOrientHelper(side)
            comm = str(t_speed) + "cl"	# crabwalk right
            print(str(values[1]), r_limit, values[2])
            #ser.write(comm.encode('utf-8'))
        myMux.disable_channels(ports[3])
        
def autoOrientHelper(side):
    global values
    
    if side == "left":
        myMux.enable_channels(ports[3])     # front left sensor
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
        
        values[3] = prox.get_proximity()
        
        myMux.enable_channels(ports[4])     # front left sensor
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
        
        values[4] = prox.get_proximity()

    if side == "right":
        myMux.enable_channels(ports[1])     # front left sensor
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
        
        values[1] = prox.get_proximity()
        
        myMux.enable_channels(ports[2])     # front left sensor
        prox = qwiic_proximity.QwiicProximity()
        prox.begin()
        
        values[2] = prox.get_proximity()
loop(1)