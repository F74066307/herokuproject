from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def hello(self,event):
        text = event.message.text
        return text.lower() == "hello"
    def on_enter_hello(self, event):
        print("Hello world")

        reply_token = event.reply_token
        send_text_message(reply_token, "hello world")
        self.go_back()

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to 歌單"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to hologura"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "go to 剪輯"

    def is_going_to_state4(self, event):
        text = event.message.text
        return text.lower() == "go to asmr"

    def is_going_to_state5(self, event):
        text = event.message.text
        return text.lower() == "go to mio"

    def is_going_to_state6(self, event):
        text = event.message.text
        return text.lower() == "go to others"
    
    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
