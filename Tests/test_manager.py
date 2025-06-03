import time
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
from .Display_Farb_Test_Gn import displayFarbTestGn
from .Display_Farb_Test_Bl import displayFarbTestBl
from .Display_Farb_Test_Rd import displayFarbTestRd
from .Touch_Test import touchTest
from .Input_Voltage_Fail_Detection_Test import inputVoltageFailTest
from .Done_Power_Off import donePowerOff
from serialCommunication import SerialCommunication
# Import other tests here

class TestManager:
    def __init__(self, app, update_status_callback, register_test_callback,run_serial_promt_test, start_button, stop_button):
        self.app = app
        self.update_status = update_status_callback
        self.register_test = register_test_callback
        self.run_serial_prompt = run_serial_promt_test
        self.serial_comm = SerialCommunication()

        
    
        self.start_button = start_button
        self.stop_button = stop_button

        #self.stop_current_test = stop_current_test

        self.serial_comm.getInfo()

        
        self.mandatory_test_names = [
            "Self Test", "Battery Change", "Activate Cylinder", "Power On", "Done/Power Off"
        ]


        # Register all tests
        self.tests = []

        
        def add_test(name, test_instance):
            self.register_test(name)
            self.tests.append((name, test_instance))

        add_test("Self Test", selfTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Battery Change", BatteryChangeTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Activate Cylinder", activateCylinder(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Power On", powerOn(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("DMM", DMM(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Load SD-Card", loadSdCard(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Status LED", statusLED(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Fan Test", fanTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Audio Test", audioTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("USB Test", usbTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("RAM Test", ramTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("SD Test", sdTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("RTC Test", rtcTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Display Color Test Green", displayFarbTestGn(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Display Color Test Blue", displayFarbTestBl(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Display Color Test Red", displayFarbTestRd(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Touch Test", touchTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Input Voltage Fail Test", inputVoltageFailTest(app, self.update_status, len(self.tests), self, self.serial_comm))
        add_test("Done/Power Off", donePowerOff(app, self.update_status, len(self.tests), self, self.serial_comm))


        # Add other tests the same way: 
        # self.register_test("Another Test")
        # self.tests.append(AnotherTest(app, self.update_status, len(self.tests)))

        self.filtered_tests = []
        self.current_test_index = 0

    def reset_test_index(self):
        self.current_test_index = 0

   


    def execute_tests(self, selected_test_names):
        
        self.filtered_tests = [
            (name, test) for name, test in self.tests
            if name in self.mandatory_test_names or name in selected_test_names
        ]

        self.reset_test_index()

        # Liste aller optionalen Tests
        all_optional_tests = [
            name for name, _ in self.tests
            if name not in self.mandatory_test_names
        ]

        # Liste der optionalen Tests, die ausgewählt wurden
        selected_optional_tests = [
            name for name in selected_test_names
            if name not in self.mandatory_test_names
        ]

        # Wenn nicht alle optionalen Tests ausgewählt wurden
        if set(selected_optional_tests) != set(all_optional_tests) and selected_optional_tests:
            # Finde den Namen des ersten optionalen Tests in der gefilterten Liste
            for i, (name, _) in enumerate(self.filtered_tests):
                if name in selected_optional_tests:
                    first_optional_index = i
                    break

            original_execute_next = self.execute_next_test

            def delayed_execute_next():
                if self.current_test_index == first_optional_index:
                    time.sleep(5)
                original_execute_next()

            self.execute_next_test = delayed_execute_next

        self.execute_next_test()




    def execute_next_test(self):
        
        if self.current_test_index < len(self.filtered_tests):
            name, current_test = self.filtered_tests[self.current_test_index]
            self.current_test_index += 1
            current_test.execute()
        else:
            print("All tests completed.")

    def stop_current_tests(self):
        if self.current_test_index > 0:
            self.filtered_tests[self.current_test_index - 1].on_fail()
