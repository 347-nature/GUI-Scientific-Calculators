"""
scientific_calculator.py

Scientific-style GUI calculator using Tkinter.
Features:
- Standard arithmetic: + - × ÷ % √ ^
- Scientific functions: sin, cos, tan, log, ln, exp, π, e
- Clear (C), Backspace (⌫), parentheses, sign toggle (±)
- Big display for results
- Keyboard support for numbers and operators

Run: python scientific_calculator.py
"""

import tkinter as tk
from tkinter import font
import math

class SciCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.resizable(False, False)
        self.expression = ""

        self._create_styles()
        self._create_widgets()

    def _create_styles(self):
        self.display_font = font.Font(family="Segoe UI", size=28, weight="bold")
        self.small_font = font.Font(family="Segoe UI", size=12)
        self.button_font = font.Font(family="Segoe UI", size=14)

    def _create_widgets(self):
        # Display
        display_frame = tk.Frame(self, padx=10, pady=10)
        display_frame.grid(row=0, column=0, sticky="nsew")

        self.expr_var = tk.StringVar(value="")
        tk.Label(display_frame, textvariable=self.expr_var, anchor="e",
                 font=self.small_font, fg="#555").pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        tk.Label(display_frame, textvariable=self.display_var, anchor="e",
                 font=self.display_font, bg="#fff", relief="sunken",
                 bd=2, padx=10, pady=10, width=20).pack(fill="both", expand=True)

        # Buttons layout
        buttons = [
            ["C", "⌫", "( )", "±", "÷"],
            ["7", "8", "9", "×", "^"],
            ["4", "5", "6", "-", "√"],
            ["1", "2", "3", "+", "%"],
            ["0", ".", "π", "e", "="]
        ]

        sci_buttons = [
            ["sin", "cos", "tan", "log", "ln"],
            ["exp", " ", " ", " ", " "]
        ]

        # Standard buttons
        btn_frame = tk.Frame(self, padx=5, pady=5)
        btn_frame.grid(row=1, column=0)

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                if label.strip() == "":
                    continue
                btn = tk.Button(btn_frame, text=label, width=5, height=2,
                                font=self.button_font,
                                command=lambda l=label: self.on_button_click(l))
                btn.grid(row=r, column=c, padx=3, pady=3)

        # Scientific buttons
        sci_frame = tk.Frame(self, padx=5, pady=5)
        sci_frame.grid(row=2, column=0)

        for r, row in enumerate(sci_buttons):
            for c, label in enumerate(row):
                if label.strip() == "":
                    continue
                btn = tk.Button(sci_frame, text=label, width=5, height=2,
                                font=self.button_font,
                                command=lambda l=label: self.on_button_click(l))
                btn.grid(row=r, column=c, padx=3, pady=3)

        # Keyboard bindings
        self.bind_all("<Return>", lambda e: self.on_button_click("="))
        self.bind_all("<BackSpace>", lambda e: self.on_button_click("⌫"))
        for key in "0123456789.+-*/()":
            self.bind_all(key, self._make_key_handler(key))

    def _make_key_handler(self, key):
        def handler(event):
            mapping = {"*": "×", "/": "÷"}
            char = mapping.get(key, key)
            self.on_button_click(char)
        return handler

    def on_button_click(self, label):
        if label == "C":
            self.expression = ""
            self.display_var.set("0")
            self.expr_var.set("")
        elif label == "⌫":
            self.expression = self.expression[:-1]
            self._refresh()
        elif label == "=":
            self.evaluate()
        elif label == "√":
            self.expression += "sqrt("
        elif label == "π":
            self.expression += str(math.pi)
        elif label == "e":
            self.expression += str(math.e)
        elif label == "^":
            self.expression += "**"
        elif label in ["sin", "cos", "tan", "log", "ln", "exp"]:
            if label == "ln":
                self.expression += "log("  # ln = natural log
            else:
                self.expression += f"{label}("
        elif label == "( )":
            if self.expression.count("(") > self.expression.count(")"):
                self.expression += ")"
            else:
                self.expression += "("
        elif label == "±":
            self.expression = f"(-1*({self.expression}))" if self.expression else ""
        else:
            self.expression += label
        self._refresh()

    def _refresh(self):
        self.expr_var.set(self.expression)
        try:
            val = self._safe_eval(self.expression.replace("×", "*").replace("÷", "/"))
            if val is not None:
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                self.display_var.set(str(val))
            else:
                self.display_var.set(self.expression or "0")
        except Exception:
            self.display_var.set(self.expression or "0")

    def evaluate(self):
        try:
            val = self._safe_eval(self.expression.replace("×", "*").replace("÷", "/"))
            if val is not None:
                if isinstance(val, float) and val.is_integer():
                    val = int(val)
                self.display_var.set(str(val))
                self.expression = str(val)
                self.expr_var.set(self.expression)
            else:
                self.display_var.set("Error")
                self.expression = ""
        except Exception:
            self.display_var.set("Error")
            self.expression = ""

    def _safe_eval(self, expr):
        try:
            allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            return eval(expr, {"__builtins__": None}, allowed)
        except Exception:
            return None


if __name__ == "__main__":
    app = SciCalculator()
    app.mainloop()