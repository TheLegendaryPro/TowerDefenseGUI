import PySimpleGUI as sg
import pyautogui

import autosend
import mouse
import json
import time

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [
    [sg.Text("Welcome to TowerDefenseGUI")],
    [sg.Button("Setup"), sg.Button("Test")],
    [sg.Button("INACTIVE", button_color="red", key="activate_button"), sg.Text("Timer: -1", key="timer_text")],
    [sg.Button("Zombie"), sg.Button("Spider"), sg.Button("Skeleton"), sg.Button("SilverFish")]
]


# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs


# Get button as variables
zombie_button = window.find_element(key="Zombie")
spider_button = window.find_element(key="Spider")
skeleton_button = window.find_element(key="Skeleton")
silver_fish_button = window.find_element(key="SilverFish")


is_active = False
active_mob = "Zombie"
timer = -1

# get cache content
# If file does not exist, create one
# If file cannot be opened as JSON, empty it and put a empty json there
global cache_content
try:
    with open("td_cache.json", mode="r") as td_cache:
        try:
            cache_content = json.load(td_cache)
        except:
            cache_content = {}
            json.dump(cache_content, td_cache, indent=4)
except:
    with open("td_cache.json", mode="w+") as td_cache:
        cache_content = {}
        json.dump(cache_content, td_cache, indent=4)

while True:
    event, values = window.read(timeout=1000)

    # Main event handler
    if event == "activate_button":
        # Change whether active or not
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
    elif event == "Setup":
        # setup the coordinates
        # ask the user to click on the two conner of the buying GUI
        # then calculate the rest of the coords
        # cache the result
        window.Hide()
        mouse.wait(mouse.LEFT)
        upper_left_x, upper_left_y = mouse.get_position()
        time.sleep(0.3)
        mouse.wait(mouse.LEFT)
        lower_right_x, lower_right_y = mouse.get_position()
        inv_box_json = {"ulx": upper_left_x,
                        "uly": upper_left_y,
                        "lrx": lower_right_x,
                        "lry": lower_right_y}
        with open("td_cache.json", mode="w+") as td_cache:
            cache_content['inv_box_json'] = inv_box_json
            json.dump(cache_content, td_cache, indent=4)
        window.UnHide()
    elif event == "Test":
        pos_matrix = []
        lrx_ = cache_content['inv_box_json']['lrx']
        ulx_ = cache_content['inv_box_json']['ulx']
        lry_ = cache_content['inv_box_json']['lry']
        uly_ = cache_content['inv_box_json']['uly']
        box_width = lrx_ - ulx_
        box_height = lry_ - uly_
        for row in range(3):
            pos_matrix.append([])
            row_height = uly_ + box_height/3*row + box_height/6
            for col in range(9):
                col_width = ulx_ + box_width/9*col + box_width/18
                pos_matrix[row].append((col_width, row_height))
                pyautogui.click(col_width, row_height)
                time.sleep(0.1)
    elif event == "Zombie":
        pass
    elif event == "Spider":
        pass
    elif event == "Skeleton":
        pass
    elif event == "SilverFish":
        pass


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
