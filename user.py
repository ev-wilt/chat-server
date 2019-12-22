class User:
    websocket = None
    current_room = -1

    def __init__(self, ws, room):
        self.websocket = ws
        self.current_room = room