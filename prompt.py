import sys
from rich.console import Console

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

class Prompt:
    def __init__(self):
        self.console = Console()
        self.current_input = ""

    def display(self):
        self.console.clear()
        self.console.print("Test Prompt (press 'q' to quit)")
        self.console.print(f"> {self.current_input}", end="")

    def run(self):
        while True:
            self.display()
            char = getch()

            if char == 'q':
                break
            elif char == '+':
                # Special key: clear the current input
                self.current_input = ""
            elif char in {'\r', '\n'}:
                # Enter key: clear the current input
                self.current_input = ""
            elif char.isprintable():
                # Echo the character and add to current input
                self.current_input += char
            
            # You can add more special key handlers here

if __name__ == "__main__":
    prompt = Prompt()
    prompt.run()