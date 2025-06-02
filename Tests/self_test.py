from guizero import Picture, Text, Box
from .base_test import BaseTest
from serialCommunication import SerialCommunication

class selfTest(BaseTest):
    def __init__(self, app, update_status, index, manager, serial_comm):
        super().__init__(app, update_status, index, manager)
        self.serial_comm = serial_comm

    def execute(self):
        self.perform_measurement()
        
    def perform_measurement(self):
        self.serial_comm.message()
        self.serial_comm.printtext()
        self.app.after(1000, self.compare_measurement_results)
    
    def compare_measurement_results(self):
        if self.serial_comm.connected == 1:
            self.complete("Passed")
            self.manager.execute_next_test()
        else:
            self.on_fail()

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()