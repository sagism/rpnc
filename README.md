rpnc

A simple reverse polish notation calculator.

## Features

- Dynamic stack length
- History navigation (arrow keys)
- Basic command mode for navigating history, etc.
- Copies last result to clipboard at exit

## Installation

    git clone https://github.com/sagism/rpnc.git
    cd rpnc
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python rpnc.py

You can install it globally on your system using pyinstaller:

    pyinstaller rpnc.py --onefile
    sudo cp dist/rpnc /usr/local/bin/

## Usage

    Supported operators: +, -, *, /, %, ^
    s - swap the last two items on the stack
    d - drop the last item from the stack
    c - clear the stack
    r - round the top of the stack (can also specifiy precision, e.g. 2r rounds to two decimal places)
    n - negate the top of the stack (toggle sign)
    h/? - show this message
    q - quit

Note that all operators are applied immediately, except for '-', which requires pressing enter as there is some ambiguity otherwise with the '-' sign for negative numbers.

## License

MIT
