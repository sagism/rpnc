import tkinter as tk

class RPNCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("RPN Calculator")
        self.stack = []
        
        # Create stack display (4 text fields stacked vertically, bottom-up order)
        self.stack_labels = []
        STACK_SIZE = 4
        for i in range(STACK_SIZE):
            stack_label = tk.Entry(root, width=20, font=('Arial', 18), justify='right', state='normal')
            stack_label.grid(row=i, column=0, columnspan=4)
            self.stack_labels.append(stack_label)

        # Create display entry for current number
        self.display = tk.Entry(root, width=20, font=('Arial', 18), justify='right', state='normal')
        self.display.grid(row=4, column=0, columnspan=4)

        # Buttons layout
        buttons = [
            ('7', 5, 0), ('8', 5, 1), ('9', 5, 2), ('/', 5, 3),
            ('4', 6, 0), ('5', 6, 1), ('6', 6, 2), ('*', 6, 3),
            ('1', 7, 0), ('2', 7, 1), ('3', 7, 2), ('-', 7, 3),
            ('0', 8, 0), ('.', 8, 1), ('+', 8, 2), ('Enter', 8, 3),
            ('AC', 9, 0), ('Swap', 9, 1), ('Drop', 9, 2), ('Undo', 9, 3),
        ]

        for (text, row, col) in buttons:
            button = tk.Button(root, text=text, width=5, height=2, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col)
        
        # Bind keyboard events
        self.root.bind('<Return>', lambda event: self.push_number())  # Enter key
        self.root.bind('<Key>', self.key_press)

    def key_press(self, event):
        if event.char.isdigit() or event.char == '.':
            self.display.config(state='normal')
            self.display.insert(tk.END, event.char)
        elif event.char in ('+', '-', '*', '/'):
            self.perform_operation(event.char)
        elif event.char == '\r':  # Enter key
            self.push_number()
        elif event.char == 'c':  # Clear (AC)
            self.clear()

        self.update_stack_display()

    def on_button_click(self, char):
        if char.isdigit() or char == '.':
            self.display.insert(tk.END, char)
        elif char == 'Enter':
            self.push_number()
        elif char in ('+', '-', '*', '/'):
            self.perform_operation(char)
        elif char == 'AC':
            self.clear()
        elif char == 'Swap':
            self.swap()
        elif char == 'Drop':
            self.drop()
        elif char == 'Undo':
            self.undo()
        self.update_stack_display()

    def push_number(self):
        number = self.display.get()
        if number:
            try:
                self.stack.append(float(number))
            except ValueError:
                pass
        self.display.delete(0, tk.END)
        self.update_stack_display()

    def perform_operation(self, operator):
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            result = 0
            if operator == '+':
                result = a + b
            elif operator == '-':
                result = a - b
            elif operator == '*':
                result = a * b
            elif operator == '/':
                if b != 0:
                    result = a / b
            self.stack.append(result)
        self.update_stack_display()

    def clear(self):
        self.stack = []
        self.display.delete(0, tk.END)
        self.update_stack_display()

    def swap(self):
        if len(self.stack) >= 2:
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        self.update_stack_display()

    def drop(self):
        if self.stack:
            self.stack.pop()
        self.update_stack_display()

    def undo(self):
        self.display.delete(0, tk.END)

    def update_stack_display(self):
        # Clear all stack labels
        for label in self.stack_labels:
            label.delete(0, tk.END)
        
        # Reverse the order of the stack display so the most recent value is at the bottom
        for i, value in enumerate(reversed(self.stack[-4:])):
            self.stack_labels[3 - i].insert(0, str(value))  # Inserting from the bottom up

if __name__ == "__main__":
    root = tk.Tk()
    calculator = RPNCalculator(root)
    root.mainloop()