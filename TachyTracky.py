import pip._vendor.requests as requests # API Calls for pulsoid
import time

# pip install pycaw

from comtypes import CLSCTX_ALL # Volume control
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import ctypes # Mouse sens

# pip install pynput

from pynput.keyboard import Key, Controller # Keyboard control

import subprocess # App kill
import psutil

def main():

    # ----------------------------------------SETUP------------------------------------

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    keyboard = Controller()

    # ---------------------------------------SETTINGS----------------------------------

    controlVolume = False
    controlMouseSens = False
    controlKeyHold = False
    controlAppKill = False

    applicationName = "" # e.g. firefox.exe, program will be killed if HR out of range

    minHR = 60 # set heartrate for mins
    maxHR = 200 # set heartrate for maxes 
    minVol = 10 # set minimum volume (0-100)
    maxVol = 100 # set maximum volume
    minSens = 1 # set minimum mouse sens (1-20)
    maxSens = 20 # set maximum mouse sens

    # -----------------------------------------API-------------------------------------

    APIKEY = "" # get key from https://pulsoid.net/ui/keys

    url = "https://dev.pulsoid.net/api/v1/data/heart_rate/latest?response_mode=text_plain_only_heart_rate"
    headers = {
        "Authorization": "Bearer " + APIKEY,
        "Content-Type": "application/json"
    }

    # ---------------------------------------FUNCTION----------------------------------

    while True:
        response = requests.get(url, headers=headers)
        print("Status Code:", response.status_code)
        print("HR: ", response.text)
        heartrate = int(response.text)

        # debug
        heartrate = 1

        if controlVolume:
            computerVolume = rangeAdjust(minHR,maxHR,minVol,maxVol,heartrate)/100
            volume.SetMasterVolumeLevelScalar(computerVolume, None)
            print("Volume: ", round(volume.GetMasterVolumeLevelScalar() * 100))

        if controlMouseSens:
            mouseSens = round(rangeAdjust(minHR,maxHR,minSens,maxSens,heartrate))
            ctypes.windll.user32.SystemParametersInfoW(113, 0, mouseSens, 0)
            print("Sens: ", mouseSens)

        if controlKeyHold and heartrate < minHR:
            keyboard.press(Key.shift)

        if controlAppKill and (heartrate > maxHR or heartrate < minHR) and checkProcessRunning(applicationName):
            print("Heartrate out of range! Killing app!")
            subprocess.call("TASKKILL /F /IM " + applicationName, shell=True)

        print()
        # time.sleep(5)

def rangeAdjust(oldMin: int, oldMax: int, newMin: int, newMax: int, val: int):
    OldRange = (oldMax - oldMin)  
    NewRange = (newMax - newMin)
    NewValue = (((val - oldMin) * NewRange) / OldRange) + newMin

    if NewValue > newMax:
        return newMax
    if NewValue < newMin:
        return newMin
    return NewValue

def checkProcessRunning(name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == name:
            return True
    return False

main()