from guizero import Picture, Text, Box, info
from .base_test import BaseTest

from GUI.popup import PopUpWindow
import threading

class touchTest(BaseTest):

    def execute(self):
        # Test in separatem Thread starten
        threading.Thread(target=self.run_test).start()

        # Hinweis für den Benutzer anzeigen
        info("Touch Test", "Touch the Touchscreen within the next 10 seconds")

    def run_test(self):
        # Prüfen, ob die serielle Verbindung verfügbar ist
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

        # Befehl senden und Ergebnis prüfen
        testResult = self.serial_comm.send_and_receive("130")

        # Ergebnis auswerten
        if testResult:
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(0, self.manager.execute_next_test)
        else:
            self.app.after(0, self.on_fail)

    def on_fail(self):
        # Fehlerbehandlung
        self.complete("Failed")
        if hasattr(self, "popup"):
            self.popup.hide()
        self.tests_complete_failed()

