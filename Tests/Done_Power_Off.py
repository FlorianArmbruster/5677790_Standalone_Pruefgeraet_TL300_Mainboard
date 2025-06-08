from guizero import Picture, Text, Box
from .base_test import BaseTest
import threading

class donePowerOff(BaseTest):

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
        testResult = self.serial_comm.send_and_receive("150")
        
        # Ergebnis auswerten
        if testResult:
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(0, self.check_all_tests_passed)
        else:
            self.app.after(0, self.on_fail)

    def check_all_tests_passed(self):
        # Nur gefilterte Tests berücksichtigen
        filtered_test_names = [name for name, _ in self.manager.filtered_tests]

        # Prüfen, ob alle relevanten Tests bestanden wurden
        all_passed = False
        all_passed = all(test["status"] == "Passed" for test in self.manager.tests_status if test["name"] in filtered_test_names)
        print(all_passed)
        if all_passed:
            self.tests_complete_pass()
            print(all_passed)

    def on_fail(self):
        # Fehlerbehandlung
        self.complete("Failed")
        self.tests_complete_failed()
    