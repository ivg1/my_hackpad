# My hackpad
A marco keyboard that I made because why not - its useful.

![view of the hackpad on startup](https://github.com/ivg1/my_hackpad/blob/main/images/main.png)
<br>
*(view of the hackpad on startup)*

## Whats required
- Pico (in my case I have the Orpheus Pico from Hack Club)
- Oled display with SH1106 driver (I have 1.3" one)
- Rotary encoder (any with A, B, GND and SW pins)
- 2x White, Green, Blue, Red LEDs
- 8x buttons
- 5x 330ohm resistors (1 for each LED)
- Wires

## Instructions
1. Wire everything together: [Schematic](https://wokwi.com/projects/451502553259884545)
2. Flash the `.uf2` file in this repo to the pico.
3. Save all the files from `src` folder onto pico.
4. You're done.

## Extra stuff
In case you use a perfboard to solder the stuff together, of 70*90mm, then you can 3d print the little case I made for it in the `models` folder.
