#from __future__ import print_function
import qwiic_bme280
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pressure, humidity, altitude, temp, pm, times, visited, x_axis = [], [], [], [], [], [], [], []
t1 = 0

mySensor = qwiic_bme280.QwiicBme280()
mySensor.begin()
mySensor.filter = 1  # 0 to 4 is valid. Filter coefficient. See 3.4.4
mySensor.standby_time = 0 # 0 to 7 valid. Time between readings. See table 27.

mySensor.over_sample = 1			# 0 to 16 are valid. 0 disables temp sensing. See table 24.
mySensor.pressure_oversample = 1	# 0 to 16 are valid. 0 disables pressure sensing. See table 23.
mySensor.humidity_oversample = 1	# 0 to 16 are valid. 0 disables humidity sensing. See table 19.
mySensor.mode = mySensor.MODE_NORMAL # MODE_SLEEP, MODE_FORCED, MODE_NORMAL is valid. See 3.3

fig, axs = plt.subplots(2, 2, sharex= True)
#plt.rcParams['figure.figsize'] = [15,11]

if mySensor.connected == False:
    print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
        file=sys.stderr)

def getDiag(node):
    global pressure, humidity, altitude, temp, pm, times, visited, x_axis
    tem = str(node[0])+","+str(node[1])
    #print(tem, x_axis)
    if tem not in x_axis:
        #if node not in visited:
        #print("here")
        #visited.append(node)
        pressure.append(mySensor.pressure/100)
        humidity.append(mySensor.humidity)
        altitude.append(mySensor.altitude_feet/(-1000))
        temp.append(mySensor.temperature_fahrenheit)
        pm.append(getAQI(mySensor.pressure))
        times.append(time.time() - t1)
        #print(len(times), len(pressure))
        #tem = ""

        x_axis.append(tem)
    #print(x_axis)

def graph():
    global pressure, humidity, altitude, temp, pm, times, x_axis
    
    #print(x_axis)
    axs[0, 0].plot(x_axis, altitude)
    axs[0, 0].set(ylabel = 'Altitude (cm)')
    
    axs[0, 1].plot(x_axis, humidity, 'tab:orange')
    axs[0, 1].set(ylabel = 'Humidity (%RH)')
    
    axs[1, 0].plot(x_axis, pm, 'tab:green')
    axs[1, 0].set(xlabel = 'Nodes (x,y)', ylabel = 'AQI (PPM)')
    axs[1, 0].set_xticklabels(x_axis, rotation = 45)
    
    axs[1, 1].plot(x_axis, temp, 'tab:red')
    axs[1, 1].set(xlabel = 'Nodes (x,y)', ylabel = 'Temp (F)')
    axs[1, 1].set_xticklabels(x_axis, rotation = 45)
    
    plt.xlabel("Node (x,y)")
    fig.suptitle('Diagnostic Data')
    
    plt.show()

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def getAQI(rawAQI):
    return map_range(rawAQI, 100000, 200000, 100, 0)-70

def runExample():
    global t1
    
    i = 0
    t1 = time.time()
    while i<5:
        curr = input("enter node")
        curr = curr.split(",")
        print("Pressure:\t%.3f" % mySensor.read_pressure())    
        
        print("Humidity:\t%.3f" % mySensor.read_humidity())

        #print("Altitude:\t%.3f" % mySensor.read_altitude())

        print("Temperature:\t%.2f" % mySensor.get_temperature_fahrenheit())
        
        print("PM 2.5:\t\t%d" % getAQI(mySensor.pressure))

        print("")
        
        getDiag(curr)
        
        i+=1

        time.sleep(1)

    graph()

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
