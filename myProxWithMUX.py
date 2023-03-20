from __future__ import print_function
import qwiic_proximity
import qwiic_tca9548a
import time
import sys

def getAllProximity():
    
    mux = qwiic_tca9548a.QwiicTCA9548A()
    
    while True:
        for i in [0, 2, 3, 4, 7]:
            mux.enable_channels(i)
            oProx = qwiic_proximity.QwiicProximity()
            oProx.begin()
            proxValue = oProx.get_proximity()
            
            toEnd = "\n" if(i==7) else "\t"
            
            #print("Sensor %d: %d" % (i, proxValue), end = toEnd)
            print("%d" % proxValue, end = toEnd)
            mux.disable_channels(i)
            #time.sleep(.01)


if __name__ == '__main__':
    try:
        getAllProximity()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
