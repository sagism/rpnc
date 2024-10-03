import os
import time
import random
import sys

def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def move_cursor(x, y):
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

def generate_random_line():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))

def update_display(stack):
    move_cursor(1, 1)
    print("\033[K" + "Stack Display Test")
    print("\033[K" + "------------------")
    for i, line in enumerate(stack, 1):
        print(f"\033[K{i}: {line}")
    print("\033[K" + "------------------")
    sys.stdout.flush()

def main():
    clear_screen()  # Clear the screen once at the start
    stack = [generate_random_line() for _ in range(3)]
    
    try:
        while True:
            update_display(stack)
            time.sleep(1)  # Wait for 1 second
            
            # Randomly update one line in the stack
            index_to_update = random.randint(0, 2)
            stack[index_to_update] = generate_random_line()
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
