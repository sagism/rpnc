import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

ARITHMETIC_OPERATORS = {'+', '-', '*', '/', '^', '%'}
UNARY_OPERATORS = {'r'}
ALL_OPERATORS = ARITHMETIC_OPERATORS | UNARY_OPERATORS

# Cross-platform getch implementation
try:
    # Windows
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
except ImportError:
    # Unix-like
    import termios
    import tty
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class RPNCalculator:
    def __init__(self):
        self.stack = []
        self.current_input = ""
        self.console = Console()

    def push(self, value):
        self.stack.append(float(value))

    def pop(self):
        return self.stack.pop() if self.stack else 0

    def perform_operation(self, op):
        if op == 'r':
            # round the top value on the stack
            if len(self.stack) < 1:
                return
            a = self.pop()
            self.console.print(f"Rounding {a} to {self.current_input} decimal places")
            if self.current_input:
                
                try:
                    precision = int(self.current_input)
                    self.console.print(f"Rounding {a} to {precision} decimal places")
                    self.push(round(a, precision))
                    self.current_input = ""
                except ValueError:
                    self.push(round(a))
            else:
                self.push(round(a))

        if self.current_input:
            self.push(self.current_input)
            self.current_input = ""

        if op in ARITHMETIC_OPERATORS:
            if len(self.stack) < 2:
                return
            b, a = self.pop(), self.pop()
            if op == '+':
                self.push(a + b)
            elif op == '-':
                self.push(a - b)
            elif op == '*':
                self.push(a * b)
            elif op == '/':
                self.push(a / b if b != 0 else float('inf'))
            elif op == '^':
                self.push(a ** b)
            elif op == '%':
                self.push(a % b)
        

            
    def display(self):
        self.console.clear()
        stack_display = "\n".join(f"{len(self.stack) - i}: {value}" for i, value in enumerate(self.stack))
        panel = Panel(
            Text(stack_display, style="bold green"),
            title="RPN Calculator",
            expand=True,
            border_style="blue",
        )
        self.console.print(panel)
        self.console.print(f"> {self.current_input}", style="bold yellow", end="")

    def run(self):
        while True:
            self.display()
            char = getch()

            if char in ALL_OPERATORS:
                self.perform_operation(char)
                self.current_input = ""
            elif char.isdigit() or char == '.':
                self.current_input += char
            elif char in {'\r', '\n'}:
                if self.current_input:
                    self.push(self.current_input)
                    self.current_input = ""
            elif char == 'd':
                if self.stack:
                    self.pop()
            elif char == 'q':
                break

if __name__ == "__main__":
    calculator = RPNCalculator()
    calculator.run()
