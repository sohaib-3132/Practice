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
        self.cursor_position = 0

        self.build_display()
        self.build_buttons()
        self.bind_keys()

        self.display.focus_set()

    def build_display(self):
        display_frame = tk.Frame(self.root, bg="#1c1e26")
        display_frame.pack(fill="both", padx=10, pady=(20, 10))

        self.display_scrollbar = tk.Scrollbar(
            display_frame,
            orient="horizontal"
        )
        self.display_scrollbar.pack(side="bottom", fill="x")

        self.display = tk.Entry(
            display_frame,
            font=("Arial", 28),
            justify="right",
            bd=0,
            bg="#1c1e26",
            fg="white",
            insertbackground="white",
            xscrollcommand=self.display_scrollbar.set
        )
        self.display.pack(side="top", fill="both", ipady=30)

        self.display_scrollbar.config(command=self.display.xview)
        self.display.bind("<ButtonRelease-1>", self.sync_cursor_from_click)

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

    def sync_cursor_from_click(self, event):
        self.cursor_position = self.display.index(tk.INSERT)

    def on_key_press(self, event):
        key = event.keysym
        char = event.char

        keypad_map = {
            "KP_0": "0", "KP_1": "1", "KP_2": "2", "KP_3": "3", "KP_4": "4",
            "KP_5": "5", "KP_6": "6", "KP_7": "7", "KP_8": "8", "KP_9": "9",
            "KP_Add": "+", "KP_Subtract": "-", "KP_Multiply": "*",
            "KP_Divide": "/", "KP_Decimal": "."
        }

        if key == "Left":
            self.move_cursor_left()
        elif key == "Right":
            self.move_cursor_right()
        elif key == "Home":
            self.move_cursor_home()
        elif key == "End":
            self.move_cursor_end()
        elif char in "0123456789":
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

    def move_cursor_left(self):
        self.cursor_position = max(0, self.cursor_position - 1)
        self.display.icursor(self.cursor_position)

    def move_cursor_right(self):
        self.cursor_position = min(len(self.expression), self.cursor_position + 1)
        self.display.icursor(self.cursor_position)

    def move_cursor_home(self):
        self.cursor_position = 0
        self.display.icursor(self.cursor_position)

    def move_cursor_end(self):
        self.cursor_position = len(self.expression)
        self.display.icursor(self.cursor_position)

    def insert_at_cursor(self, text):
        self.expression = (
            self.expression[:self.cursor_position]
            + text
            + self.expression[self.cursor_position:]
        )
        self.cursor_position += len(text)
        self.refresh_display()

    def backspace_at_cursor(self):
        if self.cursor_position > 0:
            self.expression = (
                self.expression[:self.cursor_position - 1]
                + self.expression[self.cursor_position:]
            )
            self.cursor_position -= 1
            self.refresh_display()

    def refresh_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.display.icursor(self.cursor_position)

    def on_button_click(self, symbol):
        if symbol in "0123456789":
            self.insert_at_cursor(symbol)

        elif symbol == ".":
            self.insert_at_cursor(".")

        elif symbol == "⌫":
            self.backspace_at_cursor()

        elif symbol in "+-*/":
            if self.cursor_position > 0 and self.expression[self.cursor_position - 1] not in "+-*/":
                self.insert_at_cursor(symbol)

        elif symbol == "=":
            self.calculate_result()

        elif symbol == "C":
            self.clear()

        elif symbol == "U":
            self.undo()

        elif symbol == "H":
            self.show_history()

    def tokenize(self, expression):
        tokens = []
        current_number = ""

        for char in expression:
            if char in "0123456789.":
                current_number += char
            elif char in "+-*/":
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)

        if current_number:
            tokens.append(current_number)

        return tokens

    def apply_operator(self, values_stack, operators_stack):
        operator = operators_stack.pop()
        b = values_stack.pop()
        a = values_stack.pop()

        if operator == "+":
            result = self.calculator.add(a, b)
        elif operator == "-":
            result = self.calculator.subtract(a, b)
        elif operator == "*":
            result = self.calculator.multiply(a, b)
        elif operator == "/":
            result = self.calculator.divide(a, b)

        values_stack.append(result)

    def precedence(self, operator):
        if operator in ("+", "-"):
            return 1
        if operator in ("*", "/"):
            return 2
        return 0

    def evaluate_expression(self, expression):
        tokens = self.tokenize(expression)

        values_stack = []
        operators_stack = []

        for token in tokens:
            if token not in "+-*/":
                values_stack.append(float(token))
            else:
                while (operators_stack and
                       self.precedence(operators_stack[-1]) >= self.precedence(token)):
                    self.apply_operator(values_stack, operators_stack)
                operators_stack.append(token)

        while operators_stack:
            self.apply_operator(values_stack, operators_stack)

        return values_stack[-1]

    def calculate_result(self):
        if not self.expression:
            return

        try:
            result = self.evaluate_expression(self.expression)
            self.history.add_record(self.expression, result)
            self.update_display(str(result))

        except ZeroDivisionError:
            self.update_display("Error")

        except (ValueError, IndexError):
            self.update_display("Invalid")

    def clear(self):
        self.update_display("")

    def undo(self):
        record = self.history.undo_last()
        if record:
            expression_text, result = record
            self.update_display(str(result))
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
        self.expression = value
        self.cursor_position = len(value)
        self.display.delete(0, tk.END)
        self.display.insert(0, value)
        self.display.icursor(self.cursor_position)