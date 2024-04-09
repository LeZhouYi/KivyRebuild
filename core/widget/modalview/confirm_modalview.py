from kivy.properties import StringProperty

from core.widget.modalview.color_modalview import ColorModalView


class ConfirmModalView(ColorModalView):
    input_text = StringProperty("")
    info_text = StringProperty("")

    def __init__(self, info_text: str = "", **kwargs):
        super().__init__(**kwargs)
        self.info_text = info_text
        self.init_widget()

    def init_widget(self):
        self.ids["confirm_button"].bind_event(on_tap=self.on_confirm)
        self.ids["cancel_button"].bind_event(on_tap=self.on_cancel)

    def on_confirm(self, source):
        self.dismiss()
        self.run_event("on_confirm")

    def on_cancel(self, source):
        self.dismiss()
        self.run_event("on_cancel")
