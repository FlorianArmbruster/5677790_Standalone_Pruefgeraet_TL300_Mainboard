from guizero import App, Text, PushButton, Box, yesno, Picture, CheckBox
from Tests.test_manager import TestManager
import datetime


class AppInit:
    def __init__(self):
        # App-Fenster erstellen und Vollbild aktivieren
        self.app = App(title="5677790 Standalone Prüfgerät TL300 Mainboard")
        self.app.set_full_screen()
        
        self.tests_status = []      # Liste für Testergebnisse

        # GUI-Elemente erstellen
        self.create_header()
        self.create_serial_number_input()
        self.create_test_list_header()
        self.timebox()
        # Test-Manager initialisieren
        self.test_manager = TestManager(
            self.app, 
            self.update_status, 
            self.update_test_list,
            self.update_test_list, 
            self.run_serial_number_prompt, 
            self.start_button, 
            self.stop_button, 
            self.tests_status
        )

        self.create_test_selection_ui()     # UI für Testauswahl erstellen

    def create_header(self):
        # Kopfzeile mit Logo, Titel und Schließen-Button
        header = Box(self.app, width="fill", height=30, align="top", border=True)
        header.bg = "#2691bb"
        Picture(header, image = "./Bilder/Karl_Storz_Kreis.png", align= "left", height = 25, width = 25)
        message = Text(
            header, text="5677790 Standalone Prüfgerät TL300 Mainboard", align="left"
        )
        message.text_size = 15

        close_icon = PushButton(
            header,
            image="./Bilder/Close_Icon.png",
            align="right",
            height=25,
            width=25,
            command=self.close_app      # App schließen
            )
        
    def select_all_tests(self):
        # Alle Checkboxen aktivieren
        for checkbox in self.test_checkboxes.values():
            checkbox.value = True

    def deselect_all_tests(self):
        # Alle Checkboxen deaktivieren
        for checkbox in self.test_checkboxes.values():
            checkbox.value = False
    
    
    def create_test_selection_ui(self):
        self.test_checkboxes = {}
        #Liste der Pflichttests
        mandatory_tests = [
            "Self Test", "Battery Change", "Activate Cylinder", "Power On", "Done/Power Off"
        ]

        # Container für Checkboxen
        checkbox_container = Box(self.app, layout="grid", border=True)
        row = 0
        for name, _ in self.test_manager.tests:
            if name not in mandatory_tests:
                checkbox = CheckBox(checkbox_container, text=name, grid=[0, row])
                checkbox.value = True  # Standardmäßig aktiviert
                self.test_checkboxes[name] = checkbox
                row += 1

        # Buttons für Select All / Deselect All
        control_box = Box(self.app, layout="grid", border=True)
        PushButton(control_box, text="Select All", grid=[0, 0], command=self.select_all_tests)
        PushButton(control_box, text="Deselect All", grid=[1, 0], command=self.deselect_all_tests)

    def timebox(self):
        # Box am unteren Rand für die Uhrzeit
        self.time_box = Box(self.app,width="fill", height=30, align ="bottom", border=True)
        self.time_text = Text(self.time_box,text="test", align="right")
        # Zeit jede Sekunde aktualisieren
        self.app.repeat(1000, self.time)
        self.time()
        
    def time(self):
        # Aktuelle Zeit anzeigen
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_text.value = current_time

    def create_serial_number_input(self):
        #Anzeige der eingegebenen Seriennummer
        sn_box = Box(self.app, width="fill", height=30, align="top", border=True)
        serial_number_text = Text(sn_box, text="SerialNumber:", align="left")
        serial_number_text.text_size = 20
        self.serial_number = Text(sn_box, align="left")
        self.serial_number.text_size = 20

        ssbutton_box= Box(sn_box, width= 100, height=30, align ="top")

        #Startknopf
        self.start_button = PushButton(
            ssbutton_box,
            image="./Bilder/Play_Button.png",
            align="right",
            height=25,
            width=25,
            command=self.run_serial_number_prompt,
        )
        
        #Stop Knopf
        self.stop_button = PushButton(
            ssbutton_box,
            image="./Bilder/Stop_Button.png",
            align="right",
            height=25,
            width=25,
            enabled = False,
            command=self.stop_test,
        )

        #Speichern knopf (TBI)
        self.save_icon = PushButton(
            ssbutton_box,
            image="./Bilder/Save_Icon.png",
            align="right",
            height=25,
            width=25,
        )

    def create_test_list_header(self):
        # Hauptcontainer für die Testliste
        self.test_list = Box(
            self.app, width="fill", height=30, align="top", border=True
        )
        self.test_list.bg = "#A7A7A7"

        # Linker Bereich für Testnamen
        tests_header = Box(
            self.test_list, width=200, height=30, align="left", border=True
        )

        # Rechter Bereich für Statusanzeigen
        status_header = Box(
            self.test_list, width=200, height=30, align="right", border=True
        )

        # Überschrift "Tests" im linken Bereich
        test_text = Text(tests_header, text="Tests", align="left")
        test_text.text_size = 20

        # Überschrift "Status" im rechten Bereich
        status_test = Text(status_header, text="Status", align="top")
        status_test.text_size = 20

        # Liste für dynamische Statusboxen
        self.test_status_boxes = []

    def update_test_list(self, test_name):
        # Container für einen neuen Testeintrag
        test_box = Box(self.app, width="fill", height=30, align="top", border=True)

        # Linker Bereich für den Testnamen
        test_name_box = Box(test_box, width=300, height=25, align="left")

        # Rechter Bereich für den Status
        status_box = Box(test_box, width=200, height=25, align="right", border=True)
        status_box.bg = "#eeeee4"   # Hintergrundfarbe für Statusbox

        # Textanzeige für den Testnamen
        test_text = Text(test_name_box, text=test_name, align="left", size = 15)
        # Textanzeige für den Status (initial "Pending")
        status_text = Text(status_box, text="Pending", align="top", size= 15)

        # Speichern der Statusanzeige zur späteren Aktualisierung
        self.test_status_boxes.append((status_text, status_box))
        # Speichern des Teststatus in einer Liste
        self.tests_status.append({"name": test_name, "status": "Pending"})

    def update_status(self, test_index, result):
        # Zugriff auf die Statusanzeige anhand des Index
        status_text, status_box = self.test_status_boxes[test_index]

        # Aktualisierung des Status-Textes
        status_text.value = result
        # Farbänderung je nach Ergebnis
        if result == "Passed":
            status_box.bg = "#92d51f" # #92d51f = light green
        else:
            status_box.bg = "red"

        # Aktualisierung des gespeicherten Status    
        self.tests_status[test_index]["status"] = result

    def run_serial_number_prompt(self):
        # Eingabeaufforderung für die Seriennummer
        text = self.app.question("SerialNumber", "Enter the Board SerialNumber:")
        if text is not None:
            # Seriennummer speichern
            self.serial_number.value = text
            # Teststatus zurücksetzen
            self.reset_test_status()
            # Ausgewählte Tests ermitteln
            selected_tests = [
            name for name, checkbox in self.test_checkboxes.items()
            if checkbox.value
        ]
        # Tests ausführen
        self.test_manager.execute_tests(selected_tests)
        # Buttons aktualisieren
        self.start_button.disable()
        self.stop_button.enable()

            
    def close_app(self):
         # Bestätigung zum Schließen der App
         close_prompt = yesno("Close","Do you want to close the App?")
         if close_prompt == True:  
             self.app.destroy()

    def stop_test(self):
        # Aktuelle Tests stoppen
        self.test_manager.stop_current_tests()
        # Buttons aktualisieren
        self.start_button.enable()
        self.stop_button.disable()

    def reset_test_status(self):
        # Status in der Datenstruktur zurücksetzen
        for test_status in self.tests_status:
            test_status["status"] = "Pending"

        # Statusanzeige im UI zurücksetzen
        for status_text, status_box in self.test_status_boxes:
            status_text.value = "Pending"
            status_box.bg = "#eeeee4"       

    def run(self):
        # App starten
        self.app.display()
