from guizero import Picture, Text, Box
from .base_test import BaseTest


class activateCylinder(BaseTest):

    
    def __init__(self, app, update_status, index, manager, serial_comm):
        super().__init__(app, update_status, index, manager)
        self.serial_comm = serial_comm



    def execute(self):

        
        # Prüfen, ob die serielle Verbindung verfügbar ist
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.on_fail()
            return

        # Nachricht vorbereiten 
        self.serial_comm.Texttosend = "20"
        self.serial_comm.Text_bytes = self.serial_comm.Texttosend.encode()

        self.power_cylinder()


    def power_cylinder(self):
       # self.instruction_text.value = "Measuring battery voltage..."
        
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


        self.app.after(1000, self.update_measurement_result)

    def update_measurement_result(self):
        # Simulate retrieving a measurement result
        self.measured_value = 3.7  # Here you would place your actual measurement code :D
        self.app.after(500, self.compare_measurement_results)
    
    def compare_measurement_results(self):
        if self.measured_value == 3.7:
            self.complete("Passed")
            self.manager.execute_next_test()
        else:
            self.on_fail()

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()