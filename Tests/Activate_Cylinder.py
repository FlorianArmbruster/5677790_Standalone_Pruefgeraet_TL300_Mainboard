import threading
from guizero import Picture, Text, Box
from .base_test import BaseTest

class activateCylinder(BaseTest): 

    """
    def execute(self):
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.on_fail()
            return

        # Nachricht senden und direkt auf Antwort prüfen
        #testResult = self.serial_comm.send_and_receive("20")
        testResult = True

        if testResult:
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

        # Hier kannst du später wieder send_and_receive("20") verwenden
        testResult = self.serial_comm.send_and_receive("20")
       # testResult = True  # Platzhalter für echten Test

        if testResult:
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(0, self.manager.execute_next_test)
        else:
            self.app.after(0, self.on_fail)

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()
