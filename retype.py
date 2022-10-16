import keyboard

search = (
    {"pattern": "compor",
     #    "action": ((-3,1,"rn"),(3,0,"")),
     "action": ((-3, 1, "rn"),),
     "position_correction": (0, 1, 2, 4, 5, 6, 7)
     },
    {"pattern": "linkedin.de",
     "action": ((-4, 1, "í"), (-5, 1, "í"),),
     "position_correction": tuple(range(0, 12))
     },
    {"pattern": "linkedin.com",
     "action": ((-11, 1, "1"),),
     "position_correction": tuple(range(0, 13))
     },
    {"pattern": "pea-counter",
     "action": ((-8, 1, ""), (-1, 0, "a"),),
     "position_correction": tuple(range(0, 12))
     },
    {"pattern": ", dass",
     "action": ((0, 1, ""), (-4, 1, ""),),
     "position_correction": (0, 0, 1, 2, 3, 4, 4)
     },
    {"pattern": "nämlich",
     "action": ((-5, 0, "h"),),
     "position_correction": (0, 1, 2, 4, 5, 6, 7, 8)
     },
)

# Helpful: https://pynput.readthedocs.io/en/latest/keyboard.html
# CTRL:      29
# WINDOWS_L: 91
# WINDOWS_R: 92
# ANWENDUNG: 93
# ALT:       56
# ALT_GR:    541 (Not used at the moment)
#
# Keys we want to ignore , also in combination
COMBINATION = (29, 91, 92, 93, 56)
# Wait for pressed key
current = set()
# Current stored text and cursor
text = ""
cursor = len(text)

while True:
    event = keyboard.read_event()
    if event.event_type == "down":
        if event.scan_code in COMBINATION:
            # Store modifier key
            if not event.scan_code in current:
                # print("Add modifier key")
                current.add(event.scan_code)
        else:
            # print(f"Type:         {event.event_type}")
            # print(f"Key_Pad:      {event.is_keypad}")
            # print(f"Name:         {event.name}")
            # print(f"Modifiers:    {event.modifiers}")
            # print(f"Name:         {event.name}")
            # print(f"Scan Cod      {event.scan_code}")

            if len(current):
                # print("Modifier pressed, ignoring character")
                ### Clean cursor when VTRL-V is pressed (Copy-Paste will sure kill our logic)
                if event.name == 'v' or event.name == 'V':
                    text = ""
                    cursor = len(text)
            else:
                if len(event.name) == 1:
                    text = text[:cursor] + event.name + text[cursor:]
                    cursor = cursor + 1
                else:
                    if event.scan_code == 75:  # Cursor to the left
                        cursor = cursor - 1
                        if cursor < 0:
                            # left of stored text, forget everything
                            text = ""
                            cursor = len(text)
                    elif event.scan_code == 77:  # Cursor to the right
                        cursor = cursor + 1
                        if cursor > len(text):
                            # right of stored text, forget everything
                            text = ""
                            cursor = len(text)
                    elif event.name == "entf":
                        text = text[:cursor] + text[cursor + 1:]
                    elif event.name == "backspace":
                        text = text[:cursor - 1] + text[cursor:]
                        cursor = cursor - 1
                    elif event.name == "space":
                        text = text[:cursor] + " " + text[cursor:]
                        cursor = cursor + 1
                    elif event.name == "enter" or event.scan_code == 72 or event.scan_code == 80:
                        # Enter, Arrow up or down, better clean text
                        text = ""
                        cursor = len(text)

            # print(f"Cursor {cursor} \t Text {text}")

            for pattern in search:
                # Search for pattern
                pattern_position = text.find(pattern["pattern"])
                if pattern_position >= 0:
                    # Pattern found, now try to replace
                    # Where did we start the movement?
                    start_cursor = cursor
                    # compensate for Cursor not at the end of the string
                    start_offset = pattern_position + len(pattern["pattern"]) - cursor
                    # offset ist relevant for the first movement only
                    offset = start_offset

                    for retype in pattern["action"]:
                        # retype[0]: # steps to move cursor to left or right
                        # retype[1]: # of backspace (delete text to the left
                        # retype[2]: text to inject

                        # Move Cursor
                        steps = retype[0] + offset
                        if steps < 0:
                            for x in range(steps, 0):
                                keyboard.send("left arrow")
                        elif steps > 0:
                            for x in range(0, steps):
                                keyboard.send("right arrow")
                        cursor = cursor + steps

                        # Delete Characters (Backspace)
                        for x in range(0, retype[1]):
                            keyboard.send("backspace")
                        cursor = cursor - retype[1]

                        # Write new text
                        keyboard.write(retype[2])
                        cursor = cursor + len(retype[2])

                        # offset ist relevant for the first movement only
                        offset = 0

                    # Move cursor to (corrected) start_position
                    relative_start_position = start_cursor - pattern_position
                    corrected_relative_start_position = pattern['position_correction'][relative_start_position]
                    steps = pattern_position + corrected_relative_start_position - cursor

                    if steps < 0:
                        # Move to the left
                        for x in range(steps, 0):
                            keyboard.send("left arrow")
                    elif steps > 0:
                        # Move to the right
                        for x in range(0, steps):
                            keyboard.send("right arrow")

                    # Start new search
                    text = ""
                    cursor = len(text)

    # Release of keys is only interesting to store release of combination keys (ctrl, etc...)
    elif event.event_type == "up":
        try:
            if event.scan_code in COMBINATION:
                # Delete modifier key from set of current pressed modifier keys
                current.remove(event.scan_code)
        except KeyError:
            pass
    else:
        pass
        # print("Whut?")
