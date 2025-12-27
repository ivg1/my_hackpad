"""
HID Keyboard extension module for Raspberry Pi Pico with Micropython
Original Post: (noobeepi) https://forums.raspberrypi.com/viewtopic.php?t=310876&start=50

Original Github Page: https://github.com/noobee/micropython/tree/usb-hid
MicroPython with HID v1.17 flash file: https://forums.raspberrypi.com/download/file.php?id=50270&sid=d2380350c8264368b5c082ae68bafc40

Extension written by Erdem ARSLAN
erdemsaid[:at]gmail[dot]com

Github: https://github.com/erdemarslan/hid-keyboard-micropython

Please flash noobeepi's firmware to Pico before use.

version: v.1.0
"""
import keyboard

class hidkeyboard:
    
    k = keyboard.Keyboard()
    
    # US QWERTY HID keycodes for Raspberry Pi Pico HID keyboard
    # Modifier bytes: 0xE0 - 0xE7
    # Key codes: https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

    keys = {
        # Lowercase letters
        "a": [0x04], "b": [0x05], "c": [0x06], "d": [0x07], "e": [0x08], "f": [0x09],
        "g": [0x0A], "h": [0x0B], "i": [0x0C], "j": [0x0D], "k": [0x0E], "l": [0x0F],
        "m": [0x10], "n": [0x11], "o": [0x12], "p": [0x13], "q": [0x14], "r": [0x15],
        "s": [0x16], "t": [0x17], "u": [0x18], "v": [0x19], "w": [0x1A], "x": [0x1B],
        "y": [0x1C], "z": [0x1D],

        # Uppercase letters
        "A": [k.MOD_LEFT_SHIFT, 0x04], "B": [k.MOD_LEFT_SHIFT, 0x05], "C": [k.MOD_LEFT_SHIFT, 0x06],
        "D": [k.MOD_LEFT_SHIFT, 0x07], "E": [k.MOD_LEFT_SHIFT, 0x08], "F": [k.MOD_LEFT_SHIFT, 0x09],
        "G": [k.MOD_LEFT_SHIFT, 0x0A], "H": [k.MOD_LEFT_SHIFT, 0x0B], "I": [k.MOD_LEFT_SHIFT, 0x0C],
        "J": [k.MOD_LEFT_SHIFT, 0x0D], "K": [k.MOD_LEFT_SHIFT, 0x0E], "L": [k.MOD_LEFT_SHIFT, 0x0F],
        "M": [k.MOD_LEFT_SHIFT, 0x10], "N": [k.MOD_LEFT_SHIFT, 0x11], "O": [k.MOD_LEFT_SHIFT, 0x12],
        "P": [k.MOD_LEFT_SHIFT, 0x13], "Q": [k.MOD_LEFT_SHIFT, 0x14], "R": [k.MOD_LEFT_SHIFT, 0x15],
        "S": [k.MOD_LEFT_SHIFT, 0x16], "T": [k.MOD_LEFT_SHIFT, 0x17], "U": [k.MOD_LEFT_SHIFT, 0x18],
        "V": [k.MOD_LEFT_SHIFT, 0x19], "W": [k.MOD_LEFT_SHIFT, 0x1A], "X": [k.MOD_LEFT_SHIFT, 0x1B],
        "Y": [k.MOD_LEFT_SHIFT, 0x1C], "Z": [k.MOD_LEFT_SHIFT, 0x1D],

        # Numbers
        "1": [0x1E], "2": [0x1F], "3": [0x20], "4": [0x21], "5": [0x22],
        "6": [0x23], "7": [0x24], "8": [0x25], "9": [0x26], "0": [0x27],

        # Symbols (US QWERTY)
        " ": [0x2C],
        "\n": [0x28],  # Enter
        "\b": [0x2A],  # Backspace
        "\t": [0x2B],  # Tab
        "!": [k.MOD_LEFT_SHIFT, 0x1E],  # Shift + 1
        "@": [k.MOD_LEFT_SHIFT, 0x1F],  # Shift + 2
        "#": [k.MOD_LEFT_SHIFT, 0x20],  # Shift + 3
        "$": [k.MOD_LEFT_SHIFT, 0x21],  # Shift + 4
        "%": [k.MOD_LEFT_SHIFT, 0x22],  # Shift + 5
        "^": [k.MOD_LEFT_SHIFT, 0x23],  # Shift + 6
        "&": [k.MOD_LEFT_SHIFT, 0x24],  # Shift + 7
        "*": [k.MOD_LEFT_SHIFT, 0x25],  # Shift + 8
        "(": [k.MOD_LEFT_SHIFT, 0x26],  # Shift + 9
        ")": [k.MOD_LEFT_SHIFT, 0x27],  # Shift + 0
        "-": [0x2D], "_": [k.MOD_LEFT_SHIFT, 0x2D],
        "=": [0x2E], "+": [k.MOD_LEFT_SHIFT, 0x2E],
        "[": [0x2F], "{": [k.MOD_LEFT_SHIFT, 0x2F],
        "]": [0x30], "}": [k.MOD_LEFT_SHIFT, 0x30],
        "\\": [0x31], "|": [k.MOD_LEFT_SHIFT, 0x31],
        ";": [0x33], ":": [k.MOD_LEFT_SHIFT, 0x33],
        "'": [0x34], "\"": [k.MOD_LEFT_SHIFT, 0x34],
        "`": [0x35], "~": [k.MOD_LEFT_SHIFT, 0x35],
        ",": [0x36], "<": [k.MOD_LEFT_SHIFT, 0x36],
        ".": [0x37], ">": [k.MOD_LEFT_SHIFT, 0x37],
        "/": [0x38], "?": [k.MOD_LEFT_SHIFT, 0x38],
    }


  
    def __init__(self):
        k = keyboard.Keyboard()
        
    def _find_char_and_send(self, character : str) -> None:
        global k;
        
        if character in self.keys:
            values = self.keys[character]
            
            if len(values) > 1:
                self.k.press(values[0], values[1])
            else:
                self.k.press(values[0])
            
            self.k.release_all()
    
    def write(self, string_data : str) -> None:
        for s in string_data:
            self._find_char_and_send(s)
        