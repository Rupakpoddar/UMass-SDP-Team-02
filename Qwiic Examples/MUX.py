import qwiic_tca9548a
import time
import sys

def runExample():
    print("\nSparkFun TCA9548A Example 1\n")
    test = qwiic_tca9548a.QwiicTCA9548A()

    if test.is_connected() == False:
        print("The Qwiic TCA9548A device isn't connected to the system. Please check your connection", file=sys.stderr)
        return

    try:
        test.list_channels()
        print("\n")
        time.sleep(1)

        test.enable_channels(0)
        test.list_channels()
        print("\n")
        time.sleep(1)
        
        """
        test.disable_channels([0, 2, 3])
        test.list_channels()
        print("\n")
        time.sleep(1)
        """

    except Exception as e:
            print(e)


runExample()