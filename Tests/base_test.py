from abc import ABC, abstractmethod
from guizero import  info, error, yesno





class BaseTest(ABC):
    def __init__(self, app, on_finish, test_index, manager, serial_comm):
        self.app = app
        self.on_result = on_finish
        self.test_index = test_index
        self.manager = manager
        self.result = "Pending"
        self.serial_comm = serial_comm
        self.update_test_list = manager.update_test_list

    @abstractmethod
    def execute(self):
        """Executes the test and manages the popup."""
        pass
    
    @abstractmethod
    def on_fail (self):
        """Handles Failure"""
        pass

    def complete(self, result):
        self.result = result
        #print(f"Ergebnis von Test: {self.result}")
        self.on_result(self.test_index, result)


    
    def tests_complete_pass(self):
        from .Done_Power_Off import donePowerOff
        info("Tests Passed", "The Board Passed the Tests")

        # donePowerOff registrieren und anzeigen
        power_off_test = donePowerOff(
            self.app, self.on_result, len(self.manager.tests), self.manager, self.serial_comm
        )
        self.manager.register_test("Done/Power Off")
        self.manager.tests.append(("Done/Power Off", power_off_test))
        self.manager.filtered_tests.append(("Done/Power Off", power_off_test))
        self.update_test_list("Done/Power Off")

        power_off_test.execute()

        self.start_next_board_y_n()
        self.manager.start_button.enable()
        self.manager.stop_button.disable()




    
    
    def tests_complete_failed(self):
        from .Done_Power_Off import donePowerOff
        error("Tests Failed", "The Board Failed the Tests")

        # donePowerOff vorbereiten
        power_off_test = donePowerOff(
            self.app,
            self.on_result,
            len(self.manager.tests),  # Index für GUI
            self.manager,
            self.serial_comm
        )

        # Test registrieren und in GUI anzeigen
        self.manager.register_test("Done/Power Off")
        self.manager.tests.append(("Done/Power Off", power_off_test))
        self.manager.filtered_tests.append(("Done/Power Off", power_off_test))
        self.update_test_list("Done/Power Off") 


        power_off_test.execute()

        self.start_next_board_y_n()
        self.manager.start_button.enable()
        self.manager.stop_button.disable()

    def start_next_board_y_n(self):
        next_board = yesno("Start next Bord Test", "Do you want to start the next Board test?")
        if next_board == True:
            self.manager.run_serial_prompt()