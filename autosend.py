import keyboard
import pyautogui
import time

pyautogui.MINIMUM_DURATION = 0.25

troop_dict = {
        "spider": (922 , 399)
}

def find_loc():
        current_mouse_x, current_mouse_y = pyautogui.position()
        print(str(current_mouse_x), ",", str(current_mouse_y))

def send_troop(troop_type):
        troop_x, troop_y = troop_dict[troop_type]
        pyautogui.rightClick()
        time.sleep(1)
        keyboard.press("shift")
        pyautogui.moveTo(troop_x, troop_y)
        pyautogui.click()
        keyboard.release("shift")
        time.sleep(1)
        pyautogui.moveTo(1104, 501)
        pyautogui.click()

def send_spider():
        print("sending spider")
        send_troop("spider")


spider = [927 , 392]
send = [1104 , 501]
witch = [961 , 435]