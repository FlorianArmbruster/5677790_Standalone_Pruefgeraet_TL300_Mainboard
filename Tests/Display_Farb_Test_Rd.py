from guizero import Picture, Text, Box
from .base_test import BaseTest
from GUI.popup import PopUpWindow
import threading


class displayFarbTestRd(BaseTest):
    
    def execute(self):
        # Serielle Kommunikation im Hintergrund starten
        threading.Thread(target=self.run_test).start()

        # Popup im GUI-Thread anzeigen
        self.app.after(0, self.show_popup)

    def show_popup(self):
        # Popup-Fenster konfigurieren und anzeigen
        self.popup = PopUpWindow(
            self.app,
            title="Display Color Test",
            content_box_builder=self.build_content_box,
            on_pass=self.pass_action,
            on_fail=self.on_fail,
        )
        self.popup.show()

    def run_test(self):
        # Serielle Verbindung prüfen
        if not self.serial_comm.ser or not self.serial_comm.ser.is_open:
            print("Serielle Verbindung nicht verfügbar oder nicht geöffnet.")
            self.app.after(0, self.on_fail)
            return

        # Testbefehl senden 
        testResult = self.serial_comm.send_and_receive("122")

    def build_content_box(self, parent):
        # GUI-Elemente für das Popup erstellen
        box = Box(parent, width="fill", height="fill", align="top")
        box2 = Box(box, width="fill", height="30", align="top")

        Picture(box, image="./Bilder/Rot.PNG", align="top", height=250, width=250)

        self.instruction_text = Text(
            box2, text="Display color matches color shown below:", align="top", size=20
        )

        return box

    def pass_action(self):
        # Test als bestanden markieren und fortfahren
        self.complete("Passed")
        self.popup.hide()
        self.manager.execute_next_test()

    def on_fail(self):
        # Test als fehlgeschlagen markieren
        self.complete("Failed")
        if hasattr(self, "popup"):
            self.popup.hide()
        self.tests_complete_failed()

