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
        info("Tests Passed", "The Board Passed the Tests")
        self.start_next_board_y_n()
        
        self.manager.start_button.enable()
        self.manager.stop_button.disable()



    def tests_complete_failed(self):
        error("Tests Failed","The Board Failed the Tests")
        self.start_next_board_y_n()
        
        
        self.manager.start_button.enable()
        self.manager.stop_button.disable()



    def start_next_board_y_n(self):
        next_board = yesno("Start next Bord Test", "Do you want to start the next Board test?")
        if next_board == True:
            self.manager.run_serial_prompt()