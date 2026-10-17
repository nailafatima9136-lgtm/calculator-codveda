"""
Task 1: Simple Calculator (Level 1 - Basic) — GUI Version
Built with tkinter for a clean desktop UI/UX.

Run in VS Code:
    1. Open this file.
    2. Run > Run Without Debugging (or press the ▶ button top-right).
    3. Or in the terminal: python calculator_gui.py
"""

import tkinter as tk
from tkinter import font


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.resizable(False, False)

        # ---------- Colors & Fonts (UI polish) ----------
        self.bg_color = "#1e1e2e"
        self.display_bg = "#2a2a3d"
        self.text_color = "#f5f5f5"
        self.accent = "#7c5cff"
        self.op_color = "#3a3a52"
        self.equals_color = "#7c5cff"
        self.clear_color = "#e04b4b"

        self.root.configure(bg=self.bg_color)

        self.display_font = font.Font(family="Segoe UI", size=28, weight="bold")
        self.btn_font = font.Font(family="Segoe UI", size=14)

        # ---------- State ----------
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.reset_next_input = False

        self._build_display()
        self._build_buttons()
        self._bind_keys()

    # ---------------- UI Construction ----------------

    def _build_display(self):
        display_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        display_frame.grid(row=0, column=0)

        self.expression_var = tk.StringVar(value="")
        self.expression_label = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            font=("Segoe UI", 12),
            fg="#a0a0b8",
            bg=self.bg_color,
            anchor="e",
        )
        self.expression_label.pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=self.display_font,
            fg=self.text_color,
            bg=self.display_bg,
            anchor="e",
            padx=15,
            pady=20,
            width=12,
        )
        self.display.pack(fill="x", pady=(5, 0))

    def _build_buttons(self):
        btn_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        btn_frame.grid(row=1, column=0)

        buttons = [
            ("C", 0, 0, self.clear_color, self.on_clear),
            ("←", 0, 1, self.op_color, self.on_backspace),
            ("%", 0, 2, self.op_color, lambda: self.on_operation("%")),
            ("÷", 0, 3, self.op_color, lambda: self.on_operation("/")),
            ("7", 1, 0, None, lambda: self.on_digit("7")),
            ("8", 1, 1, None, lambda: self.on_digit("8")),
            ("9", 1, 2, None, lambda: self.on_digit("9")),
            ("×", 1, 3, self.op_color, lambda: self.on_operation("*")),
            ("4", 2, 0, None, lambda: self.on_digit("4")),
            ("5", 2, 1, None, lambda: self.on_digit("5")),
            ("6", 2, 2, None, lambda: self.on_digit("6")),
            ("−", 2, 3, self.op_color, lambda: self.on_operation("-")),
            ("1", 3, 0, None, lambda: self.on_digit("1")),
            ("2", 3, 1, None, lambda: self.on_digit("2")),
            ("3", 3, 2, None, lambda: self.on_digit("3")),
            ("+", 3, 3, self.op_color, lambda: self.on_operation("+")),
            ("0", 4, 0, None, lambda: self.on_digit("0")),
            (".", 4, 1, None, self.on_decimal),
            ("=", 4, 2, self.equals_color, self.on_equals),
        ]

        for (label, row, col, color, cmd) in buttons:
            colspan = 2 if label == "=" else 1
            btn_bg = color if color else "#33334d"
            btn = tk.Button(
                btn_frame,
                text=label,
                font=self.btn_font,
                fg=self.text_color,
                bg=btn_bg,
                activebackground=self.accent,
                activeforeground="white",
                relief="flat",
                width=5 if colspan == 1 else 11,
                height=2,
                command=cmd,
                cursor="hand2",
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="nsew")

    def _bind_keys(self):
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Return>", lambda e: self.on_equals())
        self.root.bind("<BackSpace>", lambda e: self.on_backspace())

    # ---------------- Logic ----------------

    def on_key_press(self, event):
        char = event.char
        if char.isdigit():
            self.on_digit(char)
        elif char in ("+", "-", "*", "/"):
            self.on_operation(char)
        elif char == ".":
            self.on_decimal()
        elif char.lower() == "c":
            self.on_clear()

    def on_digit(self, digit):
        if self.reset_next_input:
            self.current_input = ""
            self.reset_next_input = False
        self.current_input += digit
        self._strip_leading_zero()
        self.display_var.set(self.current_input)

    def on_decimal(self):
        if self.reset_next_input:
            self.current_input = "0"
            self.reset_next_input = False
        if not self.current_input:
            self.current_input = "0"
        if "." not in self.current_input:
            self.current_input += "."
            self.display_var.set(self.current_input)

    def on_backspace(self):
        self.current_input = self.current_input[:-1]
        self.display_var.set(self.current_input if self.current_input else "0")

    def on_clear(self):
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.reset_next_input = False
        self.display_var.set("0")
        self.expression_var.set("")

    def on_operation(self, op):
        if not self.current_input and self.first_number is None:
            return  # nothing entered yet

        if self.first_number is not None and not self.reset_next_input:
            # Chain operations: compute the pending one first
            self.on_equals(chain=True)

        self.first_number = float(self.current_input or self.display_var.get())
        self.operation = op
        symbol = {"+": "+", "-": "−", "*": "×", "/": "÷", "%": "%"}[op]
        self.expression_var.set(f"{self._fmt(self.first_number)} {symbol}")
        self.reset_next_input = True

    def on_equals(self, chain=False):
        if self.operation is None or self.first_number is None:
            return
        try:
            second_number = float(self.current_input or self.display_var.get())
        except ValueError:
            self._show_error("Invalid input")
            return

        result = self._calculate(self.first_number, second_number, self.operation)

        if isinstance(result, str):  # error message, e.g. divide by zero
            self._show_error(result)
            return

        if not chain:
            symbol = {"+": "+", "-": "−", "*": "×", "/": "÷", "%": "%"}[self.operation]
            self.expression_var.set(
                f"{self._fmt(self.first_number)} {symbol} {self._fmt(second_number)} ="
            )

        self.display_var.set(self._fmt(result))
        self.current_input = self._fmt(result)
        self.first_number = result if chain else None
        if not chain:
            self.operation = None
        self.reset_next_input = True

    # ---------------- Arithmetic (Task 1 functions) ----------------

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            return "Cannot divide by zero"
        return a / b

    @staticmethod
    def modulo(a, b):
        if b == 0:
            return "Cannot divide by zero"
        return a % b

    def _calculate(self, a, b, op):
        if op == "+":
            return self.add(a, b)
        elif op == "-":
            return self.subtract(a, b)
        elif op == "*":
            return self.multiply(a, b)
        elif op == "/":
            return self.divide(a, b)
        elif op == "%":
            return self.modulo(a, b)

    # ---------------- Helpers ----------------

    def _strip_leading_zero(self):
        if self.current_input.startswith("0") and not self.current_input.startswith("0."):
            self.current_input = self.current_input.lstrip("0") or "0"

    @staticmethod
    def _fmt(value):
        if value == int(value):
            return str(int(value))
        return f"{value:.6f}".rstrip("0").rstrip(".")

    def _show_error(self, message):
        self.display_var.set(message)
        self.current_input = ""
        self.first_number = None
        self.operation = None
        self.reset_next_input = True
        # Briefly flash the display red for visual feedback
        self.display.configure(fg="#ff6b6b")
        self.root.after(1000, lambda: self.display.configure(fg=self.text_color))


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
