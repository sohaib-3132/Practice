class History:
    def __init__(self):
        self.stack = []

    def add_record(self, expression, result):
        self.stack.append((expression, result))

    def undo_last(self):
        if self.stack:
            return self.stack.pop()
        return None

    def show_history(self):
        return list(self.stack)