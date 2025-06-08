from guizero import Picture, Text, Box
from .base_test import BaseTest
from GUI.popup import PopUpWindow

class BatteryChangeTest(BaseTest):
    def execute(self):
        # Popup-Fenster für den Test anzeigen
        popup = PopUpWindow(
            self.app,
            title="Battery Change Test",
            content_box_builder=self.build_content_box,
            on_pass=self.pass_action,
            on_fail=self.on_fail,
        )
        
        self.popup = popup
        popup.show()

    def build_content_box(self, parent):
        # Layout und Inhalte des Popups erstellen
        box = Box(parent, width="fill", height="fill", align="top")
        box2 = Box(box, width="fill", height ="30", align= "top")
        box5 = Box(box, width="fill", height ="40", align= "top")
        box6 = Box(box, width="fill", height ="40", align= "top")
        box3= Box(box, width = 175, height= 20, align ="left")
        box4= Box(box, width = 175, height= 20, align ="right")

        # Bilder für falsche und richtige Batterieplatzierung
        BatteryF = Picture(box, image="./Bilder/Batterie_Falsch.JPG", align="left", height= 250, width= 250)
        BatteryR = Picture(box, image="./Bilder/Batterie_Richtig.JPG", align="right", height= 250, width= 250)

        # Hinweise und Warnungen
        self.instruction_text = Text(
            box2, text="Please ensure the battery is inserted correctly.", align="top", size= 20
        )
        self.instruction_text = Text(
            box5, text="Warning: After clicking <Pass> the Cylinder will Activate!", align="top", color= "red", font= "Impact", size= 20
        )
        self.instruction_text = Text(
            box6, text="Remove Hands from Testdevice!", align="top", color= "red", font= "Impact", size= 20
        )
        return box

    def pass_action(self):
        # Bei Erfolg: Test abschließen und nächsten starten
        self.complete("Passed")
        self.app.after(100, self.manager.execute_next_test)

    def on_fail(self):
        # Bei Fehler: Test als fehlgeschlagen markieren und Popup schließen
        self.complete("Failed")
        self.tests_complete_failed()
        self.popup.hide()
