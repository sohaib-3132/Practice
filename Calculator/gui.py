import tkinter as tk
from calculator import Calculator
from history import History


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("My Calculator")
        self.root.geometry("320x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1c1e26")

        self.calculator = Calculator()
        self.history = History()

        self.expression = ""
        self.current_operator = None
        self.first_number = None

        self.build_display()
        self.build_buttons()
        self.bind_keys()

    def build_display(self):
        self.display = tk.Entry(
            self.root,
            font=("Arial", 28),
            justify="right",
            bd=0,
            bg="#1c1e26",
            fg="white",
            insertbackground="white"
        )
        self.display.pack(fill="both", ipady=30, padx=10, pady=(20, 10))

    def build_buttons(self):
        button_frame = tk.Frame(self.root, bg="#1c1e26")
        button_frame.pack(expand=True, fill="both", padx=5, pady=5)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "⌫", "+"],
            ["C", "U", "H", "="]
        ]

        colors = {
            "operator": {"bg": "#ff9500", "hover": "#ffad33"},
            "equals": {"bg": "#4cd964", "hover": "#6fe085"},
            "clear": {"bg": "#ff3b30", "hover": "#ff6259"},
            "utility": {"bg": "#5a5f6b", "hover": "#767c8a"},
            "number": {"bg": "#2c2f38", "hover": "#3d4150"}
        }

        for row in buttons:
            row_frame = tk.Frame(button_frame, bg="#1c1e26")
            row_frame.pack(expand=True, fill="both")
            for symbol in row:
                style = self.get_style(symbol, colors)

                button = tk.Button(
                    row_frame,
                    text=symbol,
                    font=("Arial", 18, "bold"),
                    fg="white",
                    bg=style["bg"],
                    activebackground=style["hover"],
                    activeforeground="white",
                    bd=0,
                    relief=tk.FLAT,
                    command=lambda s=symbol: self.on_button_click(s)
                )
                button.pack(side="left", expand=True, fill="both", padx=3, pady=3)

                button.bind("<Enter>", lambda e, b=button, s=style: b.config(bg=s["hover"]))
                button.bind("<Leave>", lambda e, b=button, s=style: b.config(bg=s["bg"]))

    def get_style(self, symbol, colors):
        if symbol in "+-*/":
            return colors["operator"]
        elif symbol == "=":
            return colors["equals"]
        elif symbol == "C":
            return colors["clear"]
        elif symbol in ("U", "H", "⌫"):
            return colors["utility"]
        else:
            return colors["number"]

    def bind_keys(self):
        self.root.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        key = event.keysym
        char = event.char

        keypad_map = {
            "KP_0": "0", "KP_1": "1", "KP_2": "2", "KP_3": "3", "KP_4": "4",
            "KP_5": "5", "KP_6": "6", "KP_7": "7", "KP_8": "8", "KP_9": "9",
            "KP_Add": "+", "KP_Subtract": "-", "KP_Multiply": "*",
            "KP_Divide": "/", "KP_Decimal": "."
        }

        if char in "0123456789":
            self.on_button_click(char)
        elif char in "+-*/":
            self.on_button_click(char)
        elif char == ".":
            self.on_button_click(".")
        elif key in ("Return", "KP_Enter"):
            self.on_button_click("=")
        elif key == "BackSpace":
            self.on_button_click("⌫")
        elif char.lower() == "c":
            self.on_button_click("C")
        elif char.lower() == "u":
            self.on_button_click("U")
        elif char.lower() == "h":
            self.on_button_click("H")
        elif key in keypad_map:
            self.on_button_click(keypad_map[key])

    def on_button_click(self, symbol):
        if symbol in "0123456789":
            self.expression += symbol
            self.update_display(self.expression)

        elif symbol == ".":
            if "." not in self.expression:
                self.expression += "." if self.expression else "0."
                self.update_display(self.expression)

        elif symbol == "⌫":
            self.expression = self.expression[:-1]
            self.update_display(self.expression)

        elif symbol in "+-*/":
            if self.expression:
                self.first_number = float(self.expression)
                self.current_operator = symbol
                self.expression = ""

        elif symbol == "=":
            self.calculate_result()

        elif symbol == "C":
            self.clear()

        elif symbol == "U":
            self.undo()

        elif symbol == "H":
            self.show_history()

    def calculate_result(self):
        if self.first_number is None or self.current_operator is None or self.expression == "":
            return

        second_number = float(self.expression)

        try:
            if self.current_operator == "+":
                result = self.calculator.add(self.first_number, second_number)
            elif self.current_operator == "-":
                result = self.calculator.subtract(self.first_number, second_number)
            elif self.current_operator == "*":
                result = self.calculator.multiply(self.first_number, second_number)
            elif self.current_operator == "/":
                result = self.calculator.divide(self.first_number, second_number)

            expression_text = f"{self.first_number} {self.current_operator} {second_number}"
            self.history.add_record(expression_text, result)

            self.update_display(str(result))
            self.expression = str(result)
            self.first_number = None
            self.current_operator = None

        except ZeroDivisionError:
            self.update_display("Error")
            self.expression = ""
            self.first_number = None
            self.current_operator = None

    def clear(self):
        self.expression = ""
        self.first_number = None
        self.current_operator = None
        self.update_display("")

    def undo(self):
        record = self.history.undo_last()
        if record:
            expression_text, result = record
            self.update_display(str(result))
            self.expression = str(result)
        else:
            self.update_display("No history")

    def show_history(self):
        records = self.history.show_history()
        history_window = tk.Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("260x320")
        history_window.configure(bg="#1c1e26")

        if not records:
            tk.Label(history_window, text="No history yet", bg="#1c1e26", fg="white").pack(pady=10)
        else:
            for expression_text, result in records:
                tk.Label(
                    history_window,
                    text=f"{expression_text} = {result}",
                    bg="#1c1e26",
                    fg="white",
                    anchor="w"
                ).pack(fill="x", padx=10, pady=2)

    def update_display(self, value):
        self.display.delete(0, tk.END)
        self.display.insert(0, value)