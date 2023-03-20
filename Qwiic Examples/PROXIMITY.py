from __future__ import print_function
import qwiic_proximity
import time
import sys

def runExample():

    print("\nSparkFun Proximity Sensor VCN4040 Example 1\n")
    oProx = qwiic_proximity.QwiicProximity()

    if oProx.connected == False:
        print("The Qwiic Proximity device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    oProx.begin()

    while True:
        proxValue = oProx.get_proximity()
        print("Proximity Value: %d" % proxValue)
        time.sleep(.01)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)