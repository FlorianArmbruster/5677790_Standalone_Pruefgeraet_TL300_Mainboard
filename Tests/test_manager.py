from .battery_change import BatteryChangeTest
from .self_test import selfTest
from .Activate_Cylinder import activateCylinder
from .Power_On import powerOn 
from .DMM import DMM
from .Load_SD_Card import loadSdCard
from .Status_LED import statusLED
from .Fan_Test import fanTest
from .Audio_Test import audioTest
from .USB_Test import usbTest
from .RAM_Test import ramTest
from .SD_Test import sdTest
from .RTC_Test import rtcTest
from .Display_Farb_Test import displayFarbTest
from .Touch_Test import touchTest
from .Input_Voltage_Fail_Detection_Test import inputVoltageFailTest
from .Done_Power_Off import donePowerOff
from serialCommunication import SerialCommunication
# Import other tests here

class TestManager:
    def __init__(self, app, update_status_callback, register_test_callback,run_serial_promt_test):
        self.app = app
        self.update_status = update_status_callback
        self.register_test = register_test_callback
        self.run_serial_prompt = run_serial_promt_test
        self.serial_comm = SerialCommunication()
        #self.stop_current_test = stop_current_test

        # Register all tests
        self.tests = []

        self.register_test("Self Test")
        self.tests.append(selfTest(app,self.update_status, len(self.tests), self, self.serial_comm))

        self.register_test("Battery Change")
        self.tests.append(BatteryChangeTest(app, self.update_status, len(self.tests), self))

        self.register_test("Activate Cylinder")
        self.tests.append(activateCylinder(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Power On")
        self.tests.append(powerOn(app,self.update_status, len(self.tests),self))

        self.register_test("DMM")
        self.tests.append(DMM(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Load SD-Card")
        self.tests.append(loadSdCard(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Status LED")
        self.tests.append(statusLED(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Fan Test")
        self.tests.append(fanTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Audio Test")
        self.tests.append(audioTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("USB Test")
        self.tests.append(usbTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("RAM Test")
        self.tests.append(ramTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("SD Test")
        self.tests.append(sdTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("RTC Test")
        self.tests.append(rtcTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Display Color Test")
        self.tests.append(displayFarbTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Touch Test")
        self.tests.append(touchTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Input Voltage Fail Test")
        self.tests.append(inputVoltageFailTest(app,self.update_status, len(self.tests),self, self.serial_comm))

        self.register_test("Done/Power Off")
        self.tests.append(donePowerOff(app,self.update_status, len(self.tests),self, self.serial_comm))

        # Add other tests the same way: 
        # self.register_test("Another Test")
        # self.tests.append(AnotherTest(app, self.update_status, len(self.tests)))

        self.current_test_index = 0

    def reset_test_index(self):
        self.current_test_index = 0

    def execute_tests(self):
        self.reset_test_index()
        self.execute_next_test()

    def execute_next_test(self):
        if self.current_test_index < len(self.tests):
            current_test = self.tests[self.current_test_index]
            current_test.execute()
            self.current_test_index += 1
        else:
            print("All tests completed.")

    def stop_current_tests(self):
        self.tests[self.current_test_index -1].on_fail()