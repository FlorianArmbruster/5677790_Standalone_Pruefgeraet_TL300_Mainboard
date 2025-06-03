from guizero import Picture, Text, Box
from .base_test import BaseTest
from GUI.popup import PopUpWindow
import threading


class touchTest(BaseTest):

    """
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

        # Nachricht senden und auf Antwort warten
        testResult = self.serial_comm.send_and_receive("130")

        # GUI-Logik im Hauptthread
        if testResult:
            self.app.after(0, self.show_popup_and_pass)
        else:
            self.app.after(0, self.on_fail)

    def show_popup_and_pass(self):
        # Popup anzeigen
        self.popup = PopUpWindow(
            self.app,
            title="Touch Test",
            content_box_builder=self.build_content_box,
            on_pass=self.pass_action,
            on_fail=self.on_fail,
        )
        self.popup.show()

    def build_content_box(self, parent):
        box = Box(parent, width="fill", height="fill", align="top")
        box2 = Box(box, width="fill", height="30", align="top")

        Picture(box, image="./Bilder/Batterie_Falsch.JPG", align="top", height=250, width=250)

        self.instruction_text = Text(
            box2, text="Touch the Touchscreen within the next 10 seconds", align="top", size=20
        )

        return box

    def pass_action(self):
        self.complete("Passed")
        self.popup.hide()
        self.manager.execute_next_test()

    def on_fail(self):
        self.complete("Failed")
        if hasattr(self, "popup"):
            self.popup.hide()
        self.tests_complete_failed()

