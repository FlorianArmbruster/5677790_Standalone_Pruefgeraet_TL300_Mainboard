import threading
from guizero import Picture, Text, Box
from .base_test import BaseTest


#Implementierung eines Tests zur Aktivierung des Zylinders
class activateCylinder(BaseTest): 

    def execute(self):
        """Startet den Test in einem separaten Thread, um die GUI nicht zu blockieren."""

        threading.Thread(target=self.run_test).start()

    def run_test(self):
        """Führt den Test aus, indem ein Befehl über die serielle Schnittstelle gesendet wird."""

        # Überprüfen, ob die serielle Verbindung verfügbar und geöffnet ist
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

       #Befehl "20" über die serielle Schnittstelle senden und Ergenis erhalten
        testResult = self.serial_comm.send_and_receive("20")

        if testResult:
            # Wenn der Test erfolgreich war, Ergebnis setzen und nächsten Test starten
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(0, self.manager.execute_next_test)
        else:
            # Wenn der Test fehlschlägt, Fehlerbehandlung aufrufen
            self.app.after(0, self.on_fail)

    def on_fail(self):
        """Wird aufgerufen, wenn der Test fehlschlägt."""
        self.complete("Failed")
        self.tests_complete_failed()
