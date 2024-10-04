import sys



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
        # print("RPN Calculator")
        # print("==============")
        lines_printed = 0

        for i, value in enumerate(self.stack, 1):
            print(f"{len(self.stack) - i + 1}: {value}                    ")
            lines_printed += 1

        # Clear any remaining lines from previous displays
        for _ in range(lines_printed, 20):  # Assume max 20 lines for safety
            self.clear_line()
            self.move_cursor(1, _ + 1)

        # Move cursor to the input line
        self.move_cursor(1, lines_printed + 1)
        self.clear_line()
        sys.stdout.write(f"> {self.current_input}")
        sys.stdout.flush()

    def push(self, value):
        try:    
            self.stack.append(float(value))
        except ValueError:
            input(f"Invalid input: {value}\nPress Enter to continue...")

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

    def run(self):
        self.clear_screen()
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



    def run(self):
        self.clear_screen()  # Clear the screen once at the start
        while True:
            self.display()
            char = getch()

            
            if char == '-' and self.current_input == "":
                # '-' is a valid operator, but we need to check if it's a negation or a subtraction operator
                self.current_input += char
            elif char in ALL_OPERATORS:
                self.perform_operation(char)
                self.current_input = ""
            elif char.isdigit() or char == '.':
                self.current_input += char
            elif char in {'\r', '\n'}:
                if self.current_input:
                    # print(f"Processing [{self.current_input}] ...")
                    if self.current_input in ARITHMETIC_OPERATORS:
                        # print(f"Performing operation [{self.current_input}] ...")
                        self.perform_operation(self.current_input)
                    else:
                        # print(f"Pushing [{self.current_input}] ...")
                        self.push(self.current_input)
                    # input("Press Enter to continue...")
                    self.current_input = ""
            elif char == 'd':
                if self.stack:
                    self.pop()
            elif char == 'c':
                self.clear_screen() # Clear the screen
                self.stack = []
                self.current_input = ""
            elif char in ('\x08', '\x7f'):  # Backspace character (ASCII and DEL)
                if self.current_input:
                    self.current_input = self.current_input[:-1]
            elif char == 'h':
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
                print("  s: Swap top two elements")
                print("  d: Drop top element")
                print("  c: Clear")
                print("  h: Help")
                print("  q: Quit")
                input("Press Enter to continue...")
            elif char == 's':
                self.swap()
            elif char == 'q':
                self.clear_screen()  # Clear the screen before exiting
                sys.exit(0)  # Exit the program cleanly

if __name__ == "__main__":
    calculator = RPNCalculator()
    calculator.run()
