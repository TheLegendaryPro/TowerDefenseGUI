import PySimpleGUI as sg
import autosend

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [
    [sg.Button("INACTIVE", button_color="red", key="activate_button"), sg.Text("Timer: -1", key="timer_text")]
]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs

is_active = False
timer = -1

while True:
    event, values = window.read(timeout=1000)

    # Change whether active or not
    if event == "activate_button":
        activate_button = window.find_element(key="activate_button")
        is_active = activate_button.get_text() == "ACTIVE"
        if is_active:
            # deactivate
            timer = -1
            is_active = False
            activate_button.update(text="INACTIVE", button_color="red")
        else:
            # ACTIVATE
            timer = 5
            is_active = True
            activate_button.update(text="ACTIVE", button_color="green")

    if is_active:
        if timer == 0:
            autosend.send_spider()

    # THINGS TO DO AT THE END
    if timer > 0:
        timer -= 1
    elif timer == 0:
        timer = 16

    timer_text = window.find_element(key="timer_text")
    timer_text.update(value=f"Timer: {timer}")

    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

window.close()
