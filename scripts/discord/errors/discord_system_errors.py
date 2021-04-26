from typing import Dict, Any, List


class BotIsNotReady(Exception):
    def __init__(self, message='Bot was not ready when tried to invoke this function'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.message}]"
