import sys
import ast
import tty
import termios
import readline

import pyperclip



ARITHMETIC_OPERATORS = {'+', '-', '*', '/', '^', '%'}
UNARY_OPERATORS = {'r', 'n'}
ALL_OPERATORS = ARITHMETIC_OPERATORS | UNARY_OPERATORS


    
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



class RPNCalculator:
    def __init__(self):
        self.stack = []
        self.intro_message = "RPN Calculator. press h or ? for help. Enter numbers, then operators (eg 2 <enter> 3 +  to add 2 and 3)"
        self.current_input = ""
        readline.set_history_length(1000)
        self.history_offset = 0

    def clear_screen(self):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    def move_cursor(self, x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def clear_line(self):
        sys.stdout.write("\033[K")
        sys.stdout.flush()

    def swap(self):
        if len(self.stack) < 2:
            return
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def display(self):
        self.move_cursor(1, 1)
        lines_printed = 0
        if self.intro_message:
            print(self.intro_message)
            self.intro_message = ""
            lines_printed += 1

        for i, value in enumerate(self.stack, 1):
            print(f"{len(self.stack) - i + 1}: {value:,}                    ")
            lines_printed += 1

        for _ in range(lines_printed, 20):  # Assume max 20 lines for safety
            self.clear_line()
            self.move_cursor(1, _ + 1)

        # Move cursor to the input line
        self.move_cursor(1, lines_printed + 1)
        self.clear_line()
        sys.stdout.write(f"> {self.current_input}")
        sys.stdout.flush()


    def push(self, value):
        input_value = value
        try:
            if not isinstance(value, (int, float, complex)):
                value = ast.literal_eval(value)
            if not isinstance(value, (int, float, complex)):
                raise ValueError("Should be a number...")
            self.stack.append(value)
            readline.add_history(str(input_value))
            self.history_offset = 0
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Invalid input: {value}. Error: {str(e)}")

    def pop(self):
        return self.stack.pop() if self.stack else 0

    def perform_operation(self, op):
        if op == 'r':
            if len(self.stack) < 1:
                return
            a = self.pop()
            if self.current_input:
                try:
                    precision = int(self.current_input)
                    self.push(round(a, precision))
                    self.current_input = ""
                except ValueError:
                    self.push(round(a))
            else:
                self.push(round(a))
        elif op == 'n':
            if len(self.stack) < 1:
                return
            a = self.pop()
            self.push(-a)
        

        if self.current_input and self.current_input not in ALL_OPERATORS:
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
        
        self.display()  # Update the display after each operation


    def handle_up_arrow(self):
        n_history = readline.get_current_history_length()
        if n_history > 0:
            self.current_input = readline.get_history_item(n_history-self.history_offset) # n_history - self.history_index)
            self.history_offset = min(self.history_offset+1, n_history-1)

    def handle_down_arrow(self):
        n_history = readline.get_current_history_length()
        if readline.get_current_history_length() > 0:
            self.current_input = readline.get_history_item(n_history-self.history_offset)
            self.history_offset = max(self.history_offset-1, 0)


    def run(self):
        self.clear_screen()
        while True:
            self.display()
            char = getch()
            
            if char == '\x1b':  # ESC character
                next1, next2 = getch(), getch()
                if next1 == '[':
                    if next2 == 'A':  # Up arrow
                        self.handle_up_arrow()
                    elif next2 == 'B':  # Down arrow
                        self.handle_down_arrow()

            elif char == '-' and self.current_input == "":
                # '-' is a valid operator, but we need to check if it's a negation or a subtraction operator
                self.current_input += char
            elif char in ALL_OPERATORS:
                self.perform_operation(char)
                self.current_input = ""
            elif char.isdigit() or char in {'.', 'e', 'E'}:
                self.current_input += char
            elif char in {'\r', '\n'}:
                if self.current_input:
                    if self.current_input in ARITHMETIC_OPERATORS:
                        self.perform_operation(self.current_input)
                    else:
                        try:
                            self.push(self.current_input)
                        except ValueError as e:
                            input(f"\nInvalid input: {self.current_input}.\npress any key to continue...")
                    self.current_input = ""
            elif char == 'd':
                if self.stack:
                    self.pop()
            elif char == 'c':
                self.clear_screen()
                self.stack = []
                self.current_input = ""
            elif char in ('\x08', '\x7f'):  # Backspace character (ASCII and DEL)
                if self.current_input:
                    self.current_input = self.current_input[:-1]
            elif char in ('h', '?'):
                self.clear_screen()
                print("RPN Calculator")
                print("==============")
                print("Operators:")
                print("  +: Add")
                print("  -: Subtract")
                print("  *: Multiply")
                print("  /: Divide")
                print("  ^: Exponentiation")
                print("  %: Modulus")
                print("  r: Round (optionally, enter a number to specify precision, e.g. \"3r\" rounds to 3 decimal places)")
                print("  n: Negate: Toggle sign of the top element of the stack)")
                print("  s: Swap top two elements")
                print("  d: Drop top element")
                print("  c: Clear")
                print("  h/?: Help")
                print("  q: Quit")
                input("Press Enter to continue...")
            elif char == 's':
                self.swap()
            elif char == 'q':
                if len(self.stack) > 0:
                    pyperclip.copy(self.stack[0])
                self.clear_screen()  
                sys.exit(0)


if __name__ == "__main__":
    calculator = RPNCalculator()
    calculator.run()
