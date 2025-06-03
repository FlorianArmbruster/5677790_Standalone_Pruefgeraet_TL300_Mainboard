from guizero import Picture, Text, Box
from .base_test import BaseTest
import threading

class fanTest(BaseTest):

    """
    def execute(self):
        # Prüfen, ob die serielle Verbindung verfügbar ist
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.on_fail()
            return
        # Nachricht vorbereiten 
        self.serial_comm.Texttosend = "60"
        self.serial_comm.Text_bytes = self.serial_comm.Texttosend.encode()
        self.perform_measurement()

    def perform_measurement(self):
        try:
            self.serial_comm.ser.write(self.serial_comm.Text_bytes)
            data = self.serial_comm.ser.readline()
            dataDecoded = data.decode('utf-8')
            if self.serial_comm.Text in dataDecoded:
                print(dataDecoded)
        except Exception as e:
            print(f"Fehler bei der seriellen Kommunikation: {e}")
            self.on_fail()
            return

        self.app.after(1000, self.compare_measurement_results)

    #def update_measurement_result(self):
        # Simulate retrieving a measurement result
     #   self.measured_value = 3.7  # Here you would place your actual measurement code :D
     #   self.app.after(500, self.compare_measurement_results)
    
    def compare_measurement_results(self):
        if self.serial_comm.connected == 1:
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

        testResult = self.serial_comm.send_and_receive("60")
        #testResult = True  # Platzhalter für echten Test

        if testResult:
            self.app.after(0, lambda: self.complete("Passed"))
            self.app.after(0, self.manager.execute_next_test)
        else:
            self.app.after(0, self.on_fail)

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()