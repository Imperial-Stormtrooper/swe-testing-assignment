"""
Quick-Calc — A simple calculator application with a GUI.
Built with Python's built-in tkinter library (no extra installs needed).
"""

import tkinter as tk
from tkinter import font as tkfont


# ──────────────────────────────────────────────
# # Core calculation logic — pure functions, isolated from GUI, easy to unit-test
# ──────────────────────────────────────────────

def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return a - b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return a * b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return a / b.  Raises ZeroDivisionError when b == 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")  # handled gracefully in GUI
    return a / b


def calculate(a: float, operator: str, b: float) -> float:
    """Dispatch to the correct operation based on *operator* string."""
    ops = {"+": add, "-": subtract, "*": multiply, "/": divide}
    if operator not in ops:
        raise ValueError(f"Unknown operator: {operator!r}")
    return ops[operator](a, b)


# ──────────────────────────────────────────────
# GUI
# ──────────────────────────────────────────────

class QuickCalc(tk.Tk):
    """Main calculator window."""

    # Colour palette
    BG          = "#1a1a2e"   # deep navy background
    DISPLAY_BG  = "#16213e"   # slightly lighter for the display
    BTN_NUM     = "#0f3460"   # number buttons
    BTN_OP      = "#e94560"   # operator buttons (accent red)
    BTN_EQUALS  = "#e94560"
    BTN_CLEAR   = "#533483"   # clear / special
    FG          = "#eaeaea"   # general text
    DISPLAY_FG  = "#ffffff"
    HOVER_LIGHT = "#1a4a8a"   # hover for number buttons
    HOVER_OP    = "#ff6b81"   # hover for operator buttons

    def __init__(self):
        super().__init__()
        self.title("Quick-Calc")
        self.resizable(False, False)
        self.configure(bg=self.BG)

        # ── State ──────────────────────────────
        self._expression = ""   # full expression string shown on display
        self._result     = ""   # stored result after "="
        self._operator   = None
        self._first_num  = None
        self._new_input  = False  # start fresh after operator pressed

        self._build_ui()

    # ── UI construction ────────────────────────

    def _build_ui(self):
        pad = {"padx": 12, "pady": 10}

        # ── Display ────────────────────────────
        display_frame = tk.Frame(self, bg=self.DISPLAY_BG, bd=0)
        display_frame.pack(fill="x", **pad)

        self._expr_var   = tk.StringVar(value="")
        self._result_var = tk.StringVar(value="0")

        tk.Label(
            display_frame,
            textvariable=self._expr_var,
            bg=self.DISPLAY_BG, fg="#888888",
            font=("Courier New", 12), anchor="e",
            height=1
        ).pack(fill="x", padx=8, pady=(8, 0))

        tk.Label(
            display_frame,
            textvariable=self._result_var,
            bg=self.DISPLAY_BG, fg=self.DISPLAY_FG,
            font=("Courier New", 34, "bold"), anchor="e",
            height=2
        ).pack(fill="x", padx=8, pady=(0, 8))

        # ── Button grid ────────────────────────
        btn_frame = tk.Frame(self, bg=self.BG)
        btn_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Layout: (label, row, col, colspan, style)
        layout = [
            ("C",  0, 0, 1, "clear"),  ("±", 0, 1, 1, "clear"),
            ("%",  0, 2, 1, "clear"),  ("/", 0, 3, 1, "op"),
            ("7",  1, 0, 1, "num"),    ("8", 1, 1, 1, "num"),
            ("9",  1, 2, 1, "num"),    ("*", 1, 3, 1, "op"),
            ("4",  2, 0, 1, "num"),    ("5", 2, 1, 1, "num"),
            ("6",  2, 2, 1, "num"),    ("-", 2, 3, 1, "op"),
            ("1",  3, 0, 1, "num"),    ("2", 3, 1, 1, "num"),
            ("3",  3, 2, 1, "num"),    ("+", 3, 3, 1, "op"),
            ("0",  4, 0, 2, "num"),    (".", 4, 2, 1, "num"),
            ("=",  4, 3, 1, "eq"),
        ]

        for col in range(4):
            btn_frame.columnconfigure(col, weight=1, minsize=70)

        for (label, row, col, colspan, style) in layout:
            btn = self._make_button(btn_frame, label, style)
            btn.grid(row=row, column=col, columnspan=colspan,
                     sticky="nsew", padx=4, pady=4)

    def _make_button(self, parent, label: str, style: str) -> tk.Button:
        colours = {
            "num":   (self.BTN_NUM,   self.HOVER_LIGHT),
            "op":    (self.BTN_OP,    self.HOVER_OP),
            "eq":    (self.BTN_OP,    self.HOVER_OP),
            "clear": (self.BTN_CLEAR, "#7a4fbb"),
        }
        bg, hover_bg = colours.get(style, (self.BTN_NUM, self.HOVER_LIGHT))

        btn = tk.Button(
            parent, text=label,
            bg=bg, fg=self.FG,
            activebackground=hover_bg, activeforeground=self.FG,
            font=("Courier New", 16, "bold"),
            relief="flat", bd=0, cursor="hand2",
            command=lambda l=label: self._on_button(l)
        )
        # Hover effect
        btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg:       b.config(bg=c))
        return btn

    # ── Button handling ────────────────────────

    def _on_button(self, label: str):
        if label == "C":
            self._clear()
        elif label == "=":
            self._evaluate()
        elif label in ("+", "-", "*", "/"):
            self._set_operator(label)
        elif label == "±":
            self._negate()
        elif label == "%":
            self._percent()
        else:
            self._append_digit(label)

    def _clear(self):
        self._expression = ""
        self._result     = ""
        self._operator   = None
        self._first_num  = None
        self._new_input  = False
        self._result_var.set("0")
        self._expr_var.set("")

    def _append_digit(self, digit: str):
        if self._new_input:
            self._result_var.set("")
            self._new_input = False

        current = self._result_var.get()
        if current == "0" and digit != ".":
            current = ""
        if digit == "." and "." in current:
            return  # prevent double decimal
        new_val = current + digit
        self._result_var.set(new_val)

    def _set_operator(self, op: str):
        try:
            self._first_num = float(self._result_var.get())
        except ValueError:
            return
        self._operator  = op
        self._new_input = True
        self._expr_var.set(f"{self._fmt(self._first_num)} {op}")

    def _evaluate(self):
        if self._operator is None or self._first_num is None:
            return
        try:
            second = float(self._result_var.get())
            result = calculate(self._first_num, self._operator, second)
        except ZeroDivisionError:
            self._result_var.set("Error: ÷0")
            self._expr_var.set("")
            self._operator  = None
            self._first_num = None
            return
        except Exception as e:
            self._result_var.set("Error")
            return

        expr = f"{self._fmt(self._first_num)} {self._operator} {self._fmt(second)} ="
        self._expr_var.set(expr)
        self._result_var.set(self._fmt(result))
        self._operator  = None
        self._first_num = None
        self._new_input = True

    def _negate(self):
        try:
            val = float(self._result_var.get()) * -1
            self._result_var.set(self._fmt(val))
        except ValueError:
            pass

    def _percent(self):
        try:
            val = float(self._result_var.get()) / 100
            self._result_var.set(self._fmt(val))
        except ValueError:
            pass

    @staticmethod
    def _fmt(value: float) -> str:
        """Format a float: show as int if it's a whole number."""
        return str(int(value)) if value == int(value) else str(value)


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = QuickCalc()
    app.mainloop()
