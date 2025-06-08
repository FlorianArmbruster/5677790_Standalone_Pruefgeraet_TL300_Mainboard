from guizero import Picture, Text, Box
from .base_test import BaseTest
import threading

class rtcTest(BaseTest):
    
    def execute(self):
        # Starte den Test in einem separaten Thread
        threading.Thread(target=self.run_test).start()

    def run_test(self):
        # Prüfen, ob die serielle Verbindung verfügbar ist
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

        # Befehl senden und Ergebnis prüfen
        testResult = self.serial_comm.send_and_receive("110")

        # Ergebnis auswerten
        if testResult:
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(0, self.manager.execute_next_test)
        else:
            self.app.after(0, self.on_fail)

    def on_fail(self):
        # Fehlerbehandlung
        self.complete("Failed")
        self.tests_complete_failed()