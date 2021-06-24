import PySimpleGUI as sg

import autosend
import mouse
import json
import time
import winsound

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [
    [sg.Text("Welcome to TowerDefenseGUI")],
    [sg.Button("Setup"), sg.Button("INACTIVE", button_color="red", key="activate_button"), sg.Text("Timer: -1", key="timer_text"), sg.Checkbox("Auto send", key="auto_send", default=True)],
    [sg.Button("Zombie", button_color="red"), sg.Button("Spider", button_color="grey"), sg.Button("Skeleton", button_color="grey"), sg.Button("SilverFish", button_color="grey")]
]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs


# Get button as variables
zombie_button = window.find_element(key="Zombie")
spider_button = window.find_element(key="Spider")
skeleton_button = window.find_element(key="Skeleton")
silver_fish_button = window.find_element(key="SilverFish")


def reset_mob_colors():
    zombie_button.update(button_color="grey")
    spider_button.update(button_color="grey")
    skeleton_button.update(button_color="grey")
    silver_fish_button.update(button_color="grey")


is_active = False
active_mob = "Zombie"
timer = -1

# get cache content
# If file does not exist, create one
# If file cannot be opened as JSON, empty it and put a empty json there
cache_content = {}
already_setup = False
try:
    with open("td_cache.json", mode="r") as td_cache:
        try:
            cache_content = json.load(td_cache)
            already_setup = True
        except:
            cache_content = {}
            json.dump(cache_content, td_cache, indent=4)
except:
    with open("td_cache.json", mode="w+") as td_cache:
        cache_content = {}
        json.dump(cache_content, td_cache, indent=4)

pos_matrix = []


def update_pos_matrix():
    global pos_matrix
    pos_matrix = []
    lrx_ = cache_content['inv_box_json']['lrx']
    ulx_ = cache_content['inv_box_json']['ulx']
    lry_ = cache_content['inv_box_json']['lry']
    uly_ = cache_content['inv_box_json']['uly']
    box_width = lrx_ - ulx_
    box_height = lry_ - uly_
    for row in range(4):
        pos_matrix.append([])
        row_height = uly_ + box_height / 4 * row + box_height / 8
        for col in range(9):
            col_width = ulx_ + box_width / 9 * col + box_width / 18
            pos_matrix[row].append((col_width, row_height))


update_pos_matrix()
active_mob_xy = pos_matrix[0][2]
send_xy = pos_matrix[3][8]


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
        update_pos_matrix()
    elif event == "Zombie":
        reset_mob_colors()
        zombie_button.update(button_color="red")
        active_mob_xy = pos_matrix[0][2]
    elif event == "Spider":
        reset_mob_colors()
        spider_button.update(button_color="red")
        active_mob_xy = pos_matrix[0][3]
    elif event == "Skeleton":
        reset_mob_colors()
        skeleton_button.update(button_color="red")
        active_mob_xy = pos_matrix[0][4]
    elif event == "SilverFish":
        reset_mob_colors()
        silver_fish_button.update(button_color="red")
        active_mob_xy = pos_matrix[1][2]

    if is_active:
        if timer == 0:
            if already_setup:
                if window.find_element(key="auto_send").get():
                    # If the checkbox is checked
                    autosend.send_troop(active_mob_xy, send_xy)

    # THINGS TO DO AT THE END
    if timer > 0:
        timer -= 1
    elif timer == 0:
        timer = 16

    # Play notes
    if timer == 3:
        winsound.Beep(293, 300)
    elif timer == 2:
        winsound.Beep(392, 300)
    elif timer == 1:
        winsound.Beep(261, 300)

    timer_text = window.find_element(key="timer_text")
    timer_text.update(value=f"Timer: {timer}")

    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

window.close()
