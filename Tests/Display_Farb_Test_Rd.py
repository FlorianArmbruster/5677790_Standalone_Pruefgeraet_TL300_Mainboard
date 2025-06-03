from guizero import Picture, Text, Box
from .base_test import BaseTest
from GUI.popup import PopUpWindow
import threading


class displayFarbTestRd(BaseTest):
    """
    def execute(self):

        threading.Thread(target=self.run_test).start()
    
    def run_test(self):
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

        testResult = self.serial_comm.send_and_receive("122")

        popup = PopUpWindow(
            self.app,
            title="Display Color Test",
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
        
        Gruen = Picture(box, image="./Bilder/Rot.PNG", align="top", height= 250, width= 250)
        
        self.instruction_text = Text(
            box2, text="Display color matches color shown below:", align="top", size= 20
        )
       

        return box

    #def perform_measurement(self):
        #self.instruction_text.value = "Measuring battery voltage..."
        #self.app.after(2000, self.update_measurement_result)

    #def update_measurement_result(self):
        # Simulate retrieving a measurement result
        #measured_value = "3.7V"  # Here you would place your actual measurement code :D

        # Update the measurement text with the result
        #self.measurement_text.value = f"Measured Voltage: {measured_value}"
        # Generally here is your logic of a test then

    def pass_action(self):
        
        self.complete("Passed")
        self.manager.execute_next_test()

    def on_fail(self):
        self.complete("Failed")
        self.tests_complete_failed()
        self.popup.hide()
        """
    
    def execute(self):
        # Popup sofort im Hauptthread anzeigen
        self.app.after(0, self.show_popup)

        # Starte serielle Kommunikation im Hintergrund
        threading.Thread(target=self.run_test).start()

    def show_popup(self):
        self.popup = PopUpWindow(
            self.app,
            title="Display Color Test",
            content_box_builder=self.build_content_box,
            on_pass=self.pass_action,
            on_fail=self.on_fail,
        )
        self.popup.show()

    def run_test(self):
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

        # Nachricht senden und auf Antwort warten
        testResult = self.serial_comm.send_and_receive("122")

        # Optional: automatische Auswertung
        print(f"Antwort auf '122': {testResult}")
        # if testResult:
        #     self.app.after(0, self.pass_action)
        # else:
        #     self.app.after(0, self.on_fail)

    def build_content_box(self, parent):
        box = Box(parent, width="fill", height="fill", align="top")
        box2 = Box(box, width="fill", height="30", align="top")

        Picture(box, image="./Bilder/Rot.PNG", align="top", height=250, width=250)

        self.instruction_text = Text(
            box2, text="Display color matches color shown below:", align="top", size=20
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

