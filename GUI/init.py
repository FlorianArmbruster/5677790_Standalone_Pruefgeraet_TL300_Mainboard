from guizero import App, Text, PushButton, Box, yesno, Picture
from Tests.test_manager import TestManager
import datetime


class AppInit:
    def __init__(self):
        self.app = App(title="5677790 Standalone Prüfgerät TL300 Mainboard")
        self.app.set_full_screen()
        
        self.tests_status = []

        # Initialize the layout
        self.create_header()
        self.create_serial_number_input()
        self.create_test_list_header()
        self.timebox()
        self.test_manager = TestManager(
            self.app, self.update_status, self.update_test_list, self.run_serial_number_prompt, self.start_button, self.stop_button

        )

    def create_header(self):
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
            command=self.close_app
            )

    def timebox(self):
        self.time_box = Box(self.app,width="fill", height=30, align ="bottom", border=True)
        self.time_text = Text(self.time_box,text="test", align="right")
        self.app.repeat(1000, self.time)
        self.time()
        
    def time(self):
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_text.value = current_time

    def create_serial_number_input(self):
        sn_box = Box(self.app, width="fill", height=30, align="top", border=True)
        serial_number_text = Text(sn_box, text="SerialNumber:", align="left")
        serial_number_text.text_size = 20
        self.serial_number = Text(sn_box, align="left")
        self.serial_number.text_size = 20

        ssbutton_box= Box(sn_box, width= 100, height=30, align ="top")

        self.start_button = PushButton(
            ssbutton_box,
            image="./Bilder/Play_Button.png",
            align="right",
            height=25,
            width=25,
            command=self.run_serial_number_prompt,
        )
        
        self.stop_button = PushButton(
            ssbutton_box,
            image="./Bilder/Stop_Button.png",
            align="right",
            height=25,
            width=25,
            enabled = False,
            command=self.stop_test,
        )

        self.save_icon = PushButton(
            ssbutton_box,
            image="./Bilder/Save_Icon.png",
            align="right",
            height=25,
            width=25,
            #command=self.stop_serial_number_prompt,
        )

    def create_test_list_header(self):
        self.test_list = Box(
            self.app, width="fill", height=30, align="top", border=True
        )
        self.test_list.bg = "#A7A7A7"
        tests_header = Box(
            self.test_list, width=200, height=30, align="left", border=True
        )
        status_header = Box(
            self.test_list, width=200, height=30, align="right", border=True
        )

        test_text = Text(tests_header, text="Tests", align="left")
        test_text.text_size = 20

        status_test = Text(status_header, text="Status", align="top")
        status_test.text_size = 20

        # Dynamic test status list
        self.test_status_boxes = []

    def update_test_list(self, test_name):
        test_box = Box(self.app, width="fill", height=30, align="top", border=True)
        test_name_box = Box(test_box, width=300, height=25, align="left")
        status_box = Box(test_box, width=200, height=25, align="right", border=True)
        status_box.bg = "#eeeee4" 

        test_text = Text(test_name_box, text=test_name, align="left", size = 15)
        status_text = Text(status_box, text="Pending", align="top", size= 15)

        self.test_status_boxes.append((status_text, status_box))
        self.tests_status.append({"name": test_name, "status": "Pending"})

    def update_status(self, test_index, result):
        status_text, status_box = self.test_status_boxes[test_index]
        status_text.value = result
        if result == "Passed":
            status_box.bg = "#92d51f" # #92d51f = light green
        else:
            status_box.bg = "red"
        self.tests_status[test_index]["status"] = result

    def run_serial_number_prompt(self):
        text = self.app.question("SerialNumber", "Enter the Board SerialNumber:")
        if text is not None:
            self.serial_number.value = text
            self.reset_test_status()
            self.test_manager.execute_tests()
            self.start_button.disable()
            self.stop_button.enable()
            
    def close_app(self):
         close_prompt = yesno("Close","Do you want to close the App?")
         if close_prompt == True:  
             self.app.destroy()

    def stop_test(self):
        self.test_manager.stop_current_tests()
        self.start_button.enable()
        self.stop_button.disable()

    def reset_test_status(self):
        for test_status in self.tests_status:
            test_status["status"] = "Pending"

        for status_text, status_box in self.test_status_boxes:
            status_text.value = "Pending"
            status_box.bg = "#eeeee4"       

    def run(self):
        self.app.display()
