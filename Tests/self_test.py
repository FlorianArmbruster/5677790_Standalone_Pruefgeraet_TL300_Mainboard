from guizero import Picture, Text, Box
from .base_test import BaseTest
import threading


class selfTest(BaseTest):
    #def __init__(self, app, update_status, index, manager, serial_comm):
     #   super().__init__(app, update_status, index, manager)
      #  self.serial_comm = serial_comm
       # self.test_started = False
    """
    def execute(self):

        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.on_fail()
            return

        # Nachricht "10" senden und direkt auf Antwort prüfen
        testResult = self.serial_comm.send_and_receive("10")  
        #testResult = True

        if testResult == True:
            self.complete("Passed")
            self.manager.execute_next_test()
        else:
            self.on_fail()

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()
    """
    def execute(self):
        # Starte den Test in einem separaten Thread
        threading.Thread(target=self.run_test).start()

    def run_test(self):
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

        # Nachricht "10" senden und auf Antwort warten
        testResult = self.serial_comm.send_and_receive("10")

        if testResult:
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(0, self.manager.execute_next_test)
        else:
            self.app.after(0, self.on_fail)

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()
