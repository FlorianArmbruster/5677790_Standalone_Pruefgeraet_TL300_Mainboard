from guizero import Window, Box, PushButton


class PopUpWindow:
    def __init__(self, parent, title, content_box_builder, on_pass, on_fail):
        """
        :param parent: The parent app/window.
        :param title: The title of the popup window.
        :param content_box_builder: A function that builds and returns the content box.
        :param on_pass: Callback function when the "Pass" button is pressed.
        :param on_fail: Callback function when the "Fail" button is pressed.
        """
        self.window = Window(parent, title=title, height=500, width=1000)
        self.on_pass = on_pass
        self.on_fail = on_fail
        self.center_window()

        content_box = content_box_builder(self.window)
        content_box.align = "top"

        self.create_buttons()
        self.window.hide()

    def center_window(self):
        screen_width = self.window.tk.winfo_screenwidth()
        screen_height = self.window.tk.winfo_screenheight()
        x = (screen_width / 2) - (self.window.width / 2)
        y = (screen_height / 2) - (self.window.height / 2)
        self.window.tk.geometry(
            f"{self.window.width}x{self.window.height}+{int(x)}+{int(y)}"
        )

    def create_buttons(self):
        button_box = Box(
            self.window, width=500, height=100, align="bottom", border=False
        )
        pass_button = PushButton(
            button_box, command=self.pass_action, text="Pass", align="right"
        )
        fail_button = PushButton(
            button_box, command=self.fail_action, text="Fail", align="left"
        )

        pass_button.bg = "#92d51f" # #92d51f = light green
        pass_button.text_size = 20
        fail_button.bg = "red"
        fail_button.text_size = 20

    def pass_action(self):
        self.window.bg = "#92d51f" # #92d51f = light green
        self.window.after(1000, self.window.hide)
        self.window.after(1000, self.on_pass)

    def fail_action(self):
        self.window.bg = "red"
        self.window.after(1000, self.window.hide)
        self.window.after(1000, self.on_fail)

    def show(self):
        self.window.show()
        self.window.enable()
