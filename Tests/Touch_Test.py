from guizero import Picture, Text, Box
from .base_test import BaseTest
from GUI.popup import PopUpWindow


class touchTest(BaseTest):
    def execute(self):
        popup = PopUpWindow(
            self.app,
            title="Battery Change Test",
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