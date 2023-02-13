class MessageCore:
    def __init__(
            self
    ):
        self.messages = {}

    def add_message(
            self,
            message: dict
    ):
        self.messages[len(self.messages)] = message

    def get_messages(
            self
    ):
        toRet = self.messages
        self.messages = {}
        return toRet
