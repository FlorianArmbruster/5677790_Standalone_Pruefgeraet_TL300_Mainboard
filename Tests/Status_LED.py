from guizero import Picture, Text, Box
from .base_test import BaseTest
import threading

class statusLED(BaseTest):
    """
    def execute(self):
        # Prüfen, ob die serielle Verbindung verfügbar ist
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.on_fail()
            return
        
        # Nachricht senden und direkt auf Antwort prüfen
        result = self.serial_comm.send_and_receive("50")

        if result:
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
        # Prüfen, ob die serielle Verbindung verfügbar ist
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

        testResult = self.serial_comm.send_and_receive("50")
        #testResult = True  # Platzhalter für echten Test

        if testResult:
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(5000, self.manager.execute_next_test)
        else:
            self.app.after(0, self.on_fail)

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()