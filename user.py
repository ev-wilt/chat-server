class User:
    websocket = None
    current_room = -1

    def __init__(self, ws, name):
        self.websocket = ws
        self.name = name