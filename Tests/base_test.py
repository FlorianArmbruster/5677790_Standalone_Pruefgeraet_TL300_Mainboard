from abc import ABC, abstractmethod
from guizero import  info, error, yesno

# Abstrakte Basisklasse für Tests
class BaseTest(ABC):
    def __init__(self, app, on_finish, test_index, manager, serial_comm):
        self.app = app                                      # Referenz auf die GUI-Anwendung
        self.on_result = on_finish                          # Callback-Funktion, die nach Testabschluss aufgerufen wird
        self.test_index = test_index                        # Index des aktuellen Tests 
        self.manager = manager                              # Referenz auf den Testmanager
        self.result = "Pending"                             # Standardergebnis vor Testausführung
        self.serial_comm = serial_comm                      # Serielle Kommunikation mit dem Testgerät
        self.update_test_list = manager.update_test_list    # Methode zum Aktualisieren der Testliste

    @abstractmethod
    def execute(self):
        """Abstrakte Methode zur Ausführung des Tests."""
        pass
    
    @abstractmethod
    def on_fail (self):
        """Abstrakte Methode zur Behandlung eines fehlgeschlagenen Tests."""
        pass

    def complete(self, result):
        """Setzt das Testergebnis und ruft den Abschluss-Callback auf."""

        self.result = result
        #print(f"Ergebnis von Test: {self.result}")     #Debug Ausgabe
        self.on_result(self.test_index, result)

    def tests_complete_pass(self):
        """Wird aufgerufen, wenn alle Tests erfolgreich abgeschlossen wurden."""

        info("Tests Passed", "The Board Passed the Tests")

        # Start-Button aktivieren, Stop-Button deaktivieren
        self.manager.start_button.enable()
        self.manager.stop_button.disable()

        # Nachfrage, ob nächster Test gestartet werden soll
        self.start_next_board_y_n()
    
    def tests_complete_failed(self):
        """Wird aufgerufen, wenn ein Test fehlgeschlagen ist."""

        from .Done_Power_Off import donePowerOff
        error("Tests Failed", "The Board Failed the Tests")

        # donePowerOff vorbereiten
        power_off_test = donePowerOff(
            self.app,
            self.on_result,
            len(self.manager.tests),
            self.manager,
            self.serial_comm
        )
        
        # donePowerOff ausführen wenn Test fehlgeschlagen
        power_off_test.execute()

        # Start-Button aktivieren, Stop-Button deaktivieren
        self.manager.start_button.enable()
        self.manager.stop_button.disable()

        # Nachfrage, ob nächster Test gestartet werden soll
        self.start_next_board_y_n()


    def start_next_board_y_n(self):
        """Fragt den Benutzer, ob der nächste Test gestartet werden soll."""
        
        next_board = False
        #Popup anzeigen
        next_board = yesno("Start next Bord Test", "Do you want to start the next Board test?")

        if next_board == True:
            # Start-Button deaktivieren, Stop-Button aktivieren
            self.manager.start_button.disable()
            self.manager.stop_button.enable()
            self.manager.run_serial_prompt()    # Startet den nächsten Test

        # Start-Button aktivieren, Stop-Button deaktivieren
        if next_board == False:
            self.manager.start_button.enable()
            self.manager.stop_button.disable()
            
