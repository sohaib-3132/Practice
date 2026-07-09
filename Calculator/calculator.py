class Calculator:
    def __init__(self):
        self.last_result = None

    def add(self, a, b):
        self.last_result = a + b
        return self.last_result

    def subtract(self, a, b):
        self.last_result = a - b
        return self.last_result

    def multiply(self, a, b):
        self.last_result = a * b
        return self.last_result

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.last_result = a / b
        return self.last_result