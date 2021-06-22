import keyboard
import pyautogui
import time

pyautogui.MINIMUM_DURATION = 0.25


def send_troop(troop_xy, send_xy):
        troop_x, troop_y = troop_xy
        pyautogui.rightClick()
        time.sleep(1)
        keyboard.press("shift")
        pyautogui.moveTo(troop_x, troop_y)
        pyautogui.click()
        keyboard.release("shift")
        time.sleep(1)
        send_x, send_y = send_xy
        pyautogui.moveTo(send_x, send_y)
        pyautogui.click()