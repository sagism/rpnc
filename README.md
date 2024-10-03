rpnc

A simple reverse polish notation calculator.

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
    d - drop the last item from the stack
    q - quit
    r - round the top of the stack
    2r - round to two number of decimal places (you can use any number)

## License

MIT
