from machine import Pin, I2C
from rp2 import PIO, StateMachine, asm_pio
import time
import sh1106
import klavye
from keyboard import Keyboard as Keys

# init HID keyboard
k = klavye.hidkeyboard()

# volume stuff
def volume_up():
    k.k.press(Keys.MOD_RIGHT_GUI, Keys.MOD_RIGHT_SHIFT, k.keys["a"][0])
    k.k.release_all()
    k.k.press(Keys.MOD_RIGHT_GUI, Keys.MOD_RIGHT_SHIFT, k.keys["a"][0])
    k.k.release_all()

def volume_down():
    k.k.press(Keys.MOD_RIGHT_GUI, Keys.MOD_RIGHT_SHIFT, k.keys["b"][0])
    k.k.release_all()
    k.k.press(Keys.MOD_RIGHT_GUI, Keys.MOD_RIGHT_SHIFT, k.keys["b"][0])
    k.k.release_all()

# oled
i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400_000)
oled = sh1106.SH1106_I2C(128, 64, i2c)
oled.rotate(True)
oled.fill(0)
oled.show()

# leds
red = Pin(20, Pin.OUT)
blue = Pin(21, Pin.OUT)
green = Pin(22, Pin.OUT)

white1 = Pin(16, Pin.OUT)
white2 = Pin(17, Pin.OUT)

white_leds_state = False
white1.value(0)
white2.value(0)

def blink_all_leds():
    white1.value(1)
    white2.value(1)
    green.value(1)
    blue.value(1)
    red.value(1)
    time.sleep_ms(1000)
    if not white_leds_state:
        white1.value(0)
        white2.value(0)
    green.value(0)
    blue.value(0)
    red.value(0)

# buttons
enc_button = Pin(28, Pin.IN, Pin.PULL_UP)

def enc_button_pressed():
    if enc_button.value() == 0:
        blue.value(1)
        time.sleep_ms(25)
        blue.value(0)
        return enc_button.value() == 0
    return False

btn1 = Pin(2, Pin.IN, Pin.PULL_UP)
btn2 = Pin(3, Pin.IN, Pin.PULL_UP)
btn3 = Pin(4, Pin.IN, Pin.PULL_UP)
btn4 = Pin(5, Pin.IN, Pin.PULL_UP)
btn5 = Pin(6, Pin.IN, Pin.PULL_UP)
btn6 = Pin(7, Pin.IN, Pin.PULL_UP)
btn7 = Pin(8, Pin.IN, Pin.PULL_UP)
btn8 = Pin(9, Pin.IN, Pin.PULL_UP)

btn_cmds = [
    "ssh -p 6768 ivangar@46.199.193.30\n",
    (Keys.MOD_LEFT_ALT, 0x2B),
    "3",
    "4",
    "5",
    "6",
    "7",
    "8"
]


def btn_led_blink():
    green.value(1)
    time.sleep_ms(100)
    green.value(0)

def check_btn_pressed():
    if btn1.value() == 0:
        green.value(1)
        k.k.press(Keys.MOD_LEFT_GUI, k.keys["r"][0])
        k.k.release_all()
        time.sleep_ms(300)
        enter_data(btn_cmds[0], True)
        green.value(0)
        time.sleep_ms(250)
    if btn2.value() == 0:
        green.value(1)
        for i in btn_cmds[1]:
            k.k.press(i)
        k.k.release_all()
        time.sleep_ms(100)
        green.value(0)
        time.sleep_ms(250)
    if btn3.value() == 0:
        green.value(1)
        enter_data(btn_cmds[2], True)
        time.sleep_ms(100)
        green.value(0)
        time.sleep_ms(250)
    if btn4.value() == 0:
        green.value(1)
        enter_data(btn_cmds[3], True)
        time.sleep_ms(100)
        green.value(0)
        time.sleep_ms(250)
    if btn5.value() == 0:
        green.value(1)
        enter_data(btn_cmds[4], True)
        time.sleep_ms(100)
        green.value(0)
        time.sleep_ms(250)
    if btn6.value() == 0:
        green.value(1)
        enter_data(btn_cmds[5], True)
        time.sleep_ms(100)
        green.value(0)
        time.sleep_ms(250)
    if btn7.value() == 0:
        green.value(1)
        enter_data(btn_cmds[6], True)
        time.sleep_ms(100)
        green.value(0)
        time.sleep_ms(250)
    if btn8.value() == 0:
        green.value(1)
        enter_data(btn_cmds[7], True)
        time.sleep_ms(100)
        green.value(0)
        time.sleep_ms(250)

# 

# inputs
def enter_data(data, only_text):
    if only_text:
        k.write(data)
    else:
        k.k.press(Keys.MOD_RIGHT_GUI, Keys.MOD_RIGHT_SHIFT, k.keys[data][0])
        k.k.release_all()
        k.k.press(Keys.MOD_RIGHT_GUI, Keys.MOD_RIGHT_SHIFT, k.keys[data][0])
        k.k.release_all()

# encoder
@asm_pio(in_shiftdir=PIO.SHIFT_LEFT, autopush=True, push_thresh=32)
def encoder_pio():
    wrap_target()
    in_(pins, 2)
    wrap()

pin_a = Pin(26, Pin.IN, Pin.PULL_UP)
pin_b = Pin(27, Pin.IN, Pin.PULL_UP)

sm = StateMachine(0, encoder_pio, in_base=pin_a, freq=1000000)
sm.active(1)

CW  = (0b0001, 0b0111, 0b1110, 0b1000)
CCW = (0b0010, 0b0100, 0b1101, 0b1011)

last_state = None
tick = 0

# encoder handling
def handle_rotation(direction):
    global selected
    if screen in ["menu", "commands", "passwords", "settings"]:
        menu_len = len(current_menu)
        selected = (selected + direction) % menu_len
        draw_menu(current_menu)
    elif screen == "volume":
        if direction > 0:
            volume_up()
        else:
            volume_down()

def update_encoder():
    global last_state, tick
    if sm.rx_fifo():
        state = sm.get() & 0b11
        if last_state is None:
            last_state = state
            return
        trans = (last_state << 2) | state
        if trans in CW:
            tick += 1
        elif trans in CCW:
            tick -= 1
        
        if tick >= 2:
            red.value(1)
            handle_rotation(1)
            tick = 0
            red.value(0)
        elif tick <= -2:
            red.value(1)
            handle_rotation(-1)
            tick = 0
            red.value(0)
        last_state = state


# menus
visible_items = 4

main_menu = [
    ("Change volume", "volume"),
    ("Commands", "commands"),
    ("Passwords", "passwords"),
    ("Settings", "settings"),
    ("About", "about"),
    ("Screensaver", "screensaver")
]

commands_menu = [
    ("<- Back", "back"),
    ("Open VSCode", "c"),
    ("Brave browser", "d"),
    ("Connect server", "connect_server", "ssh -p 6768 ivangar@46.199.193.30\n"),
    ("{unassigned}", " "),
    ("{unassigned}", " "),
    ("{unassigned}", " "),
]

passwords_menu = [
    ("<- Back", "back"),
    ("Test1", "abs0lut3_cin3m@\n"),
    ("Test2", "123456password_pakistan\n")
]

settings_menu = [
    ("<- Back", "back"),
    ("Toggle White", "toggle_white_leds"),
    ("BlinkAll LEDs", "blink_all_leds")
    
]

current_menu = main_menu
selected = 0

#shows screensaver on boot. change to menu if want
screen = "screensaver"

# draw functions for all frames
def draw_menu(menu):
    oled.fill(0)
    start = max(0, min(selected - visible_items // 2, len(menu) - visible_items))
    for i in range(start, min(start + visible_items, len(menu))):
        y = (i - start) * 16
        text = menu[i][0]
        if i == selected:
            oled.fill_rect(0, y, 128, 16, 1)
            oled.text(text, 2, y + 4, 0)
        else:
            oled.text(text, 2, y + 4, 1)
    oled.show()

def draw_volume():
    oled.fill(0)
    oled.text("Volume control", 0, 16)
    oled.text("Turn knob", 0, 32)
    oled.text("Press to exit", 0, 48)
    oled.show()

def draw_about():
    oled.fill(0)
    oled.text("Ivan's Hackpad", 0, 2)
    oled.text("On Orpheus Pico", 0, 16)
    oled.text("copyright 2025", 0, 50)
    oled.show()

def draw_screensaver():
    oled.fill(0)
    oled.text("Ivan's Hackpad", 7, 32)
    oled.show()
    
# main loop
# draw_menu(current_menu)
draw_screensaver()
blink_all_leds()

while True:
    update_encoder()

    if enc_button_pressed():
        item_action = current_menu[selected][1]

        if screen == "menu":
            if item_action == "volume":
                screen = "volume"
                draw_volume()
            elif item_action == "commands":
                screen = "commands"
                current_menu = commands_menu
                selected = 0
                draw_menu(current_menu)
            elif item_action == "passwords":
                screen = "passwords"
                current_menu = passwords_menu
                selected = 0
                draw_menu(current_menu)
            elif item_action == "settings":
                screen = "settings"
                current_menu = settings_menu
                selected = 0
                draw_menu(current_menu)
            elif item_action == "about":
                screen = "about"
                draw_about()
            elif item_action == "screensaver":
                screen = "screensaver"
                draw_screensaver()
        elif screen == "volume":
            screen = "menu"
            current_menu = main_menu
            selected = 0
            draw_menu(current_menu)
        elif screen == "commands":
            if item_action == "back":
                screen = "menu"
                current_menu = main_menu
                selected = 1
            elif item_action == "connect_server":
                k.k.press(Keys.MOD_LEFT_GUI, k.keys["r"][0])
                k.k.release_all()
                time.sleep_ms(300)
                enter_data(current_menu[selected][2], True)
            else:
                enter_data(item_action, False)
                #oled.fill(0)
                #oled.text("Command executed", 0, 32)
                #oled.show()
                #time.sleep_ms(500)
            draw_menu(current_menu)
        elif screen == "passwords":
            if item_action == "back":
                screen = "menu"
                current_menu = main_menu
                selected = 2
            else:
                enter_data(item_action, True)
                #oled.fill(0)
                #oled.text("Password entered", 0, 32)
                #oled.show()
                #time.sleep_ms(500)
            draw_menu(current_menu)
        elif screen == "settings":
            if item_action == "back":
                screen = "menu"
                current_menu = main_menu
                selected = 3
            elif item_action == "toggle_white_leds":
                if not white_leds_state:
                    white1.value(1)
                    white2.value(1)
                    white_leds_state = True
                else:
                    white1.value(0)
                    white2.value(0)
                    white_leds_state = False
            elif item_action == "blink_all_leds":
                blink_all_leds()
            draw_menu(current_menu)
        elif screen == "about":
            screen = "menu"
            current_menu = main_menu
            selected = 4
            draw_menu(current_menu)
        elif screen == "screensaver":
            screen = "menu"
            current_menu = main_menu
            selected = 0
            draw_menu(current_menu)

        time.sleep_ms(250)
        
    check_btn_pressed()

    time.sleep_ms(1)

