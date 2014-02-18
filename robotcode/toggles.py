class Toggle:
    def __init__(self, boolean_callable, on_repeated=int, off_repeated=int, on_toggle=int, off_toggle=int, description=""):
        self.bool_call = boolean_callable
        self.on_repeated = on_repeated # Using int() as a near-instant callable with no side effects
        self.off_repeated = off_repeated
        self.on_toggle = on_toggle
        self.off_toggle = off_toggle
        self.toggle_pressed = False
        self.toggle_on = False
        self.description = description
    def update(self):
        if not self.toggle_pressed and self.bool_call():
            self.toggle_on = not self.toggle_on
            if self.toggle_on:
                self.on_toggle()
            else:
                self.off_toggle()
            print(self.toggle_on, self.description)
            self.toggle_pressed = True
        elif not self.bool_call():
            self.toggle_pressed = False
        if self.toggle_on:
            self.on()
        else:
           self.off()