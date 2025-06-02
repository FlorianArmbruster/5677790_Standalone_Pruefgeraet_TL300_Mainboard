from guizero import Picture, Text, Box
from .base_test import BaseTest
from GUI.popup import PopUpWindow


class touchTest(BaseTest):
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
        self.serial_comm.Texttosend = "130"
        self.serial_comm.Text_bytes = self.serial_comm.Texttosend.encode()

        popup = PopUpWindow(
            self.app,
            title="Touch Test",
            content_box_builder=self.build_content_box,
            on_pass=self.pass_action,
            on_fail=self.on_fail,
        )
        
        self.popup = popup
        popup.show()

        #self.perform_measurement()

    def build_content_box(self, parent):
        
        box = Box(parent, width="fill", height="fill", align="top")
        box2 = Box(box, width="fill", height ="30", align= "top")
        
        BatteryF = Picture(box, image="./Bilder/Batterie_Falsch.JPG", align="top", height= 250, width= 250)
        
        self.instruction_text = Text(
            box2, text="Touch the Touchscreen within the next 10 seconds", align="top", size= 20
        )
       # self.measurement_text = Text(
       #     box, text="Waiting for measurement...", align="top"
       # )

        return box

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

    def compare_measurement_results(self):
        if self.serial_comm.connected == 1:
            self.complete("Passed")
            self.manager.execute_next_test()
        else:
            self.on_fail()

    def pass_action(self):
        self.complete("Passed")
        self.manager.execute_next_test()

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()
        self.popup.hide()