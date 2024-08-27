from guizero import Picture, Text, Box
from .base_test import BaseTest

class rtcTest(BaseTest):
    def execute(self):
        self.perform_measurement()

    def perform_measurement(self):
       # self.instruction_text.value = "Measuring battery voltage..."
        self.app.after(1000, self.update_measurement_result)

    def update_measurement_result(self):
        # Simulate retrieving a measurement result
        self.measured_value = 3.7  # Here you would place your actual measurement code :D
        self.app.after(500, self.compare_measurement_results)
    
    def compare_measurement_results(self):
        if self.measured_value == 3.7:
            self.complete("Passed")
            self.manager.execute_next_test()
        else:
            self.complete("Failed")