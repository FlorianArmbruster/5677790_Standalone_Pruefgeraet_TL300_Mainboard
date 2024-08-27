from abc import ABC, abstractmethod


class BaseTest(ABC):
    def __init__(self, app, on_finish, test_index, manager):
        self.app = app
        self.on_result = on_finish
        self.test_index = test_index
        self.manager = manager
        self.result = "Pending"

    @abstractmethod
    def execute(self):
        """Executes the test and manages the popup."""
        pass

    def complete(self, result):
        self.result = result
        self.on_result(self.test_index, result)
