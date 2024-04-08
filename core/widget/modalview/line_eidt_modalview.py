from kivy.properties import StringProperty

from core.widget.input import ColorTextInput  # type: ignore
from core.widget.modalview import ColorModalView


class LineEditModalView(ColorModalView):
    input_text = StringProperty("")
    info_text = StringProperty("")

    def __init__(self, input_text: str = "", info_text: str = "", **kwargs):
        super().__init__(**kwargs)
        self.input_text = input_text
        self.info_text = info_text
        self.init_widget()

    def init_widget(self):
        self.ids["confirm_button"].bind_event(on_tap=self.on_confirm)
        self.ids["cancel_button"].bind_event(on_tap=self.on_cancel)

    def on_confirm(self, source):
        self.dismiss()
        self.input_text = self.ids["text_input"].text
        self.run_event("on_confirm")

    def on_cancel(self, source):
        self.dismiss()
        self.run_event("on_cancel")
