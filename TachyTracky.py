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

    controlVolume = False # map heartrate to computer volume
    controlMouseSens = False # map heartrate to mouse sensitivity
    controlKeyHold = False # hold a key if heartrate too low
    controlAppKill = False # kill game if heartrate out of range
    controlShutdown = False # shut down computer if heartrate out of range

    key = Key.shift # e.g. Key.shift or 'c' 
    applicationName = "" # e.g. firefox.exe, program will be killed if HR out of range

    minHR, maxHR = 60, 200 # set mins and maxes for HR
    minVol, maxVol = 10, 100 # set mins and maxes for volume (0-100)
    minSens, maxSens = 1, 20 # set mins and maxes for mouse sense (1-20)

    # -----------------------------------------API-------------------------------------

    APIKEY = "" # get key from https://pulsoid.net/ui/keys

    url = "https://dev.pulsoid.net/api/v1/data/heart_rate/latest?response_mode=text_plain_only_heart_rate"
    headers = {
        "Authorization": "Bearer " + APIKEY,
        "Content-Type": "application/json"
    }

    # ---------------------------------------FUNCTION----------------------------------

    while True:
        try:
            response = requests.get(url, headers=headers)
            print("Status Code:", response.status_code)
            print("HR:", response.text)
            heartrate = int(response.text)

            if controlVolume:
                computerVolume = rangeAdjust(minHR,maxHR,minVol,maxVol,heartrate)/100
                volume.SetMasterVolumeLevelScalar(computerVolume, None)
                print("Volume:", round(volume.GetMasterVolumeLevelScalar() * 100))

            if controlMouseSens:
                mouseSens = round(rangeAdjust(minHR,maxHR,minSens,maxSens,heartrate))
                ctypes.windll.user32.SystemParametersInfoW(113, 0, mouseSens, 0)
                print("Sens:", mouseSens)

            if controlKeyHold and heartrate < minHR:
                keyboard.press(key)
                print("Holding", key.name)

            if controlAppKill and (heartrate > maxHR or heartrate < minHR) and checkProcessRunning(applicationName):
                subprocess.call("TASKKILL /F /IM " + applicationName, shell=True)
                print("Heartrate out of range! Killing", applicationName)

            if controlShutdown and heartrate < minHR:
                subprocess.call("SHUTDOWN -P", shell=True)

        except Exception as e:
            print("Error fetching HR")

        print()

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

if __name__ == "__main__":
    main()